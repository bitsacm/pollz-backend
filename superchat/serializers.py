from rest_framework import serializers
from .models import SuperChat

class SuperChatSerializer(serializers.ModelSerializer):
    class Meta:
        model=SuperChat
        fields=['id','user','message','amount','created_at','payment_status']
        
    user = serializers.StringRelatedField() 