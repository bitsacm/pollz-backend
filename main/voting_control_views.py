from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import VotingSession

# ========== VOTING CONTROL ENDPOINTS ==========

@api_view(['GET'])
@permission_classes([AllowAny])
def get_voting_status(request, voting_type):
    """
    Get current voting status for a specific voting type
    Returns voting status and appropriate message for display
    """
    try:
        voting_session = VotingSession.objects.get(voting_type=voting_type)
        status_info, message = voting_session.get_current_status()
        
        return Response({
            'voting_type': voting_type,
            'status': status_info,
            'message': message,
            'is_voting_allowed': voting_session.is_voting_allowed(),
            'session_name': voting_session.name,
            'start_time': voting_session.voting_start_time,
            'end_time': voting_session.voting_end_time,
        })
    except VotingSession.DoesNotExist:
        return Response({
            'voting_type': voting_type,
            'status': 'inactive',
            'message': 'Voting session not configured.',
            'is_voting_allowed': False,
            'session_name': None,
            'start_time': None,
            'end_time': None,
        })

@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_voting_statuses(request):
    """
    Get voting status for all configured voting types
    """
    statuses = {}
    voting_types = ['su_election', 'huel_voting', 'department_club']
    
    for voting_type in voting_types:
        try:
            voting_session = VotingSession.objects.get(voting_type=voting_type)
            status_info, message = voting_session.get_current_status()
            statuses[voting_type] = {
                'status': status_info,
                'message': message,
                'is_voting_allowed': voting_session.is_voting_allowed(),
                'session_name': voting_session.name,
                'start_time': voting_session.voting_start_time,
                'end_time': voting_session.voting_end_time,
            }
        except VotingSession.DoesNotExist:
            statuses[voting_type] = {
                'status': 'inactive',
                'message': 'Voting session not configured.',
                'is_voting_allowed': False,
                'session_name': None,
                'start_time': None,
                'end_time': None,
            }
    
    return Response(statuses)