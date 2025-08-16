from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import transaction
from .models import SuperChat
from django.conf import settings
from .serializers import SuperChatSerializer
import razorpay
import json
import hmac
import hashlib
import logging
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import F
from datetime import timedelta

logger = logging.getLogger(__name__)
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_order(request):
    try:
        data = request.data
        amount = int(data.get('amount', 0))
        message = data.get('message', '')

        logger.info(f"Received create_order request: amount={amount}, message={message}")

        if amount <= 0:
            return Response({'error': 'Invalid amount'}, status=400)

        if not message:
            return Response({'error': 'Message is required'}, status=400)

        order_currency = 'INR'
        order_receipt = f'order_rcptid_{request.user.id}_{SuperChat.objects.count() + 1}'

        logger.info(f"Creating Razorpay order: amount={amount}, currency={order_currency}, receipt={order_receipt}")
        
        order = client.order.create(dict(
            amount=amount * 100,  # Amount in paise
            currency=order_currency,
            receipt=order_receipt,
            payment_capture='1',
            notes={
                'message': message,
                'user_id': str(request.user.id)
            }
        ))

        superchat = SuperChat.objects.create(
            user_id=request.user.id,
            message=message,
            amount=amount,
            order_id=order['id'],
            payment_status='pending',
        )

        logger.info(f"Razorpay order created and stored: {order}")

        return Response({
            'order_id': order['id'],
            'amount': order['amount'],
            'currency': order['currency']
        })
    except Exception as e:
        logger.error(f"Unexpected error in create_order: {str(e)}", exc_info=True)
        return Response({'error': f'An unexpected error occurred: {str(e)}'}, status=500)
@csrf_exempt
@api_view(["POST"])
def razorpay_webhook(request):
    try:
        received_signature = request.headers.get('X-Razorpay-Signature')
        if not received_signature:
            return Response({'error': 'No Razorpay signature found in request'}, status=400)

        webhook_secret = settings.RAZORPAY_WEBHOOK_SECRET
        
        expected_signature = hmac.new(
            webhook_secret.encode(),
            request.body,
            hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(received_signature, expected_signature):
            logger.warning("Invalid Razorpay webhook signature")
            return Response({'error': 'Invalid signature'}, status=400)

        payload = json.loads(request.body)
        
        if payload['event'] == 'payment.captured':
            order_id = payload['payload']['payment']['entity']['order_id']
            payment_id = payload['payload']['payment']['entity']['id']

            # Retrieve the order details from Razorpay
            order_details = client.order.fetch(order_id)
            razorpay_message = order_details['notes'].get('message', '')

            try:
                superchat = SuperChat.objects.get(order_id=order_id)
                superchat.payment_status = 'captured'
                superchat.payment_id = payment_id
                
                # If the message is missing in our database, use the one from Razorpay
                if not superchat.message and razorpay_message:
                    superchat.message = razorpay_message
                
                superchat.save()
            except SuperChat.DoesNotExist:
                # If the SuperChat object doesn't exist, create it with data from Razorpay
                user_id = int(order_details['notes'].get('user_id', 0))
                SuperChat.objects.create(
                    user_id=user_id,
                    message=razorpay_message,
                    amount=order_details['amount'] / 100,  # Convert from paise to rupees
                    order_id=order_id,
                    payment_id=payment_id,
                    payment_status='captured'
                )

            return Response({'status': 'Payment captured successfully'}, status=200)

        return Response({'status': 'Unhandled event'}, status=400)

    except Exception as e:
        logger.error(f"Error in Razorpay webhook: {str(e)}", exc_info=True)
        return Response({'error': 'An error occurred'}, status=500)

@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def get_super_chats(request):
    # now = timezone.now()
    # SuperChat.objects.filter(payment_status='captured', is_expired=False, created_at__lt=now - timedelta(hours=24)).update(is_expired=True)    
    super_chats = SuperChat.objects.filter(payment_status='captured', is_expired=False).order_by('-amount')    
    serializer = SuperChatSerializer(super_chats, many=True)
    return Response(serializer.data)