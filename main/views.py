from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Q, Sum, Avg, Count
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
import requests

from .models import (
    ElectionPosition, ElectionCandidate, AnonymousElectionVote,
    Department, Huel, HuelRating, HuelComment,
    DepartmentClub, DepartmentClubVote, DepartmentClubComment,
    UserProfile
)
from .serializers import (
    UserSerializer, UserProfileSerializer,
    ElectionPositionSerializer, ElectionCandidateSerializer, AnonymousElectionVoteSerializer,
    DepartmentSerializer, HuelSerializer, HuelRatingSerializer, HuelCommentSerializer,
    DepartmentClubSerializer, DepartmentClubVoteSerializer, DepartmentClubCommentSerializer,
    VotingStatsSerializer
)
from rest_framework_simplejwt.exceptions import TokenError

# ========== UTILITY FUNCTIONS ==========

def get_token_for_user(user):
    tokens = RefreshToken.for_user(user)
    return tokens

def get_or_create_user_profile(user, google_data=None):
    """Get or create user profile with Google data"""
    profile, created = UserProfile.objects.get_or_create(
        user=user,
        defaults={
            'google_id': google_data.get('id') if google_data else None,
            'picture': google_data.get('picture', '') if google_data else '',
            'is_verified': True if google_data else False
        }
    )
    return profile

# ========== AUTHENTICATION VIEWS ==========

@api_view(["POST"])
def google_login(request):
    """Enhanced Google login with user profile creation"""
    try:
        access_token = request.data.get("access_token")
        
        if not access_token:
            return Response({"error": "access_token is required"}, status=400)

        # Get user profile from Google
        profile_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"
        headers = {"Authorization": f"Bearer {access_token}"}
        profile_info_response = requests.get(profile_info_url, headers=headers)

        if not profile_info_response.ok:
            return Response({"error": "Invalid token"}, status=400)

        profile_info = profile_info_response.json()
        email = profile_info["email"]

        # Check if user exists
        try:
            user = User.objects.get(email=email)
            profile = get_or_create_user_profile(user, profile_info)
            message = "User already registered. Signing in..."
        except User.DoesNotExist:
            # Create new user
            user = User.objects.create(
                username=profile_info["id"],
                email=email,
                first_name=profile_info.get("given_name", ""),
                last_name=profile_info.get("family_name", "")
            )
            profile = get_or_create_user_profile(user, profile_info)
            message = "User registered successfully."

        # Generate JWT tokens
        tokens = get_token_for_user(user)
        user_data = UserProfileSerializer(profile, context={'request': request}).data

        return Response({
            "message": message,
            "user": user_data,
            "tokens": {
                "refresh": str(tokens),
                "access": str(tokens.access_token),
            }
        }, status=200)

    except Exception as e:
        return Response({"error": str(e)}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """User logout with token blacklisting"""
    try:
        refresh_token = request.data.get('refresh_token')
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"success": "Successfully logged out."}, status=205)
    except TokenError:
        return Response({"error": "Invalid token"}, status=400)
    except Exception as e:
        return Response({"error": str(e)}, status=400)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """Get current user profile"""
    try:
        profile = get_or_create_user_profile(request.user)
        serializer = UserProfileSerializer(profile, context={'request': request})
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

# ========== ELECTION VIEWS ==========

@api_view(["GET"])
def election_positions(request):
    """List all active election positions"""
    positions = ElectionPosition.objects.filter(is_active=True)
    serializer = ElectionPositionSerializer(positions, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(["GET"])
def election_candidates(request):
    """List all candidates with optional position filtering"""
    position_id = request.GET.get('position')
    
    candidates = ElectionCandidate.objects.filter(is_active=True)
    if position_id:
        candidates = candidates.filter(position_id=position_id)
    
    candidates = candidates.select_related('position').order_by('-vote_count')
    serializer = ElectionCandidateSerializer(candidates, many=True, context={'request': request})
    return Response(serializer.data)



@api_view(["POST"])
@permission_classes([IsAuthenticated])
def cast_anonymous_election_vote(request):
    """Cast an anonymous vote for an election candidate"""
    try:
        candidate_id = request.data.get('candidate_id')
        if not candidate_id:
            return Response({"error": "candidate_id is required"}, status=400)

        candidate = get_object_or_404(ElectionCandidate, id=candidate_id, is_active=True)
        
        # Create anonymous voter hash
        voter_hash = AnonymousElectionVote.create_voter_hash(
            request.user.id, 
            candidate.position.id
        )
        
        # Check if this anonymous voter already voted for this position
        existing_vote = AnonymousElectionVote.objects.filter(
            voter_hash=voter_hash, 
            position=candidate.position
        ).first()
        
        if existing_vote:
            return Response({
                "error": f"You have already voted for {candidate.position.name}"
            }, status=400)

        # Get client IP for basic fraud prevention (hashed)
        client_ip = request.META.get('HTTP_X_FORWARDED_FOR')
        if client_ip:
            client_ip = client_ip.split(',')[0].strip()
        else:
            client_ip = request.META.get('REMOTE_ADDR')
        
        ip_hash = AnonymousElectionVote.hash_ip(client_ip)
        
        # Create anonymous vote
        from django.utils import timezone
        vote_time = timezone.now()
        
        vote_signature = AnonymousElectionVote.create_vote_signature(
            voter_hash,
            candidate.id,
            vote_time.isoformat()
        )
        
        anonymous_vote = AnonymousElectionVote.objects.create(
            voter_hash=voter_hash,
            candidate=candidate,
            position=candidate.position,
            vote_signature=vote_signature,
            ip_hash=ip_hash
        )
        
        # Update candidate vote count (using anonymous votes)
        anonymous_vote_count = candidate.anonymous_votes.count()
        candidate.vote_count = anonymous_vote_count
        candidate.save()
        
        # Update user profile voting status flags
        profile = get_or_create_user_profile(request.user)
        if candidate.position.name.lower() == "president":
            profile.voted_president = True
        elif candidate.position.name.lower() in ["general secretary", "gensec"]:
            profile.voted_gen_sec = True
        profile.save()

        return Response({
            "success": f"Anonymous vote cast successfully for {candidate.name}",
            "vote_id": anonymous_vote.id,
            "voter_id": voter_hash[:8],  # Only first 8 chars for identification
            "verification": {
                "signature": vote_signature,
                "timestamp": vote_time.isoformat()
            }
        })

    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def check_anonymous_vote_status(request):
    """Check if user has voted anonymously for any positions"""
    try:
        positions = ElectionPosition.objects.filter(is_active=True)
        vote_status = {}
        
        for position in positions:
            voter_hash = AnonymousElectionVote.create_voter_hash(
                request.user.id, 
                position.id
            )
            has_voted = AnonymousElectionVote.objects.filter(
                voter_hash=voter_hash, 
                position=position
            ).exists()
            
            vote_status[position.id] = {
                'position_name': position.name,
                'has_voted': has_voted,
                'voter_id': voter_hash[:8] if has_voted else None
            }
        
        return Response({
            "vote_status": vote_status,
            "privacy_notice": "Your votes are completely anonymous and cannot be traced back to you."
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status=500)

# ========== HUEL VIEWS ==========

@api_view(["GET"])
def departments(request):
    """List all departments"""
    departments = Department.objects.all()
    serializer = DepartmentSerializer(departments, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def huels(request):
    """List huels with search and filter options"""
    search = request.GET.get('search', '')
    department = request.GET.get('department')
    sort_by = request.GET.get('sort_by', 'overall')  # overall, grading, toughness, upvotes
    
    huels = Huel.objects.filter(is_active=True).select_related('department').prefetch_related('comments')
    
    # Search filter
    if search:
        huels = huels.filter(
            Q(code__icontains=search) |
            Q(name__icontains=search) |
            Q(instructor__icontains=search)
        )
    
    # Department filter
    if department:
        huels = huels.filter(department__short_name=department)
    
    # Sorting
    if sort_by == 'grading':
        huels = huels.order_by('-avg_grading')
    elif sort_by == 'toughness':
        huels = huels.order_by('avg_toughness')  # Lower toughness first
    elif sort_by == 'upvotes':
        huels = huels.order_by('-upvotes')
    else:  # overall
        huels = huels.order_by('-avg_overall')
    
    serializer = HuelSerializer(huels, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(["GET"])
def huel_detail(request, huel_id):
    """Get detailed huel information"""
    huel = get_object_or_404(Huel, id=huel_id, is_active=True)
    serializer = HuelSerializer(huel, context={'request': request})
    return Response(serializer.data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def rate_huel(request):
    """Rate a huel course"""
    try:
        huel_id = request.data.get('huel_id')
        grading = request.data.get('grading')
        toughness = request.data.get('toughness')
        overall = request.data.get('overall')
        
        if not all([huel_id, grading, toughness, overall]):
            return Response({
                "error": "huel_id, grading, toughness, and overall ratings are required"
            }, status=400)
        
        huel = get_object_or_404(Huel, id=huel_id, is_active=True)
        
        # Update or create rating
        rating, created = HuelRating.objects.update_or_create(
            user=request.user,
            huel=huel,
            defaults={
                'grading': float(grading),
                'toughness': float(toughness),
                'overall': float(overall)
            }
        )
        
        # Update huel aggregated ratings
        huel.update_ratings()
        
        action = "created" if created else "updated"
        return Response({
            "success": f"Rating {action} successfully",
            "rating": HuelRatingSerializer(rating).data
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def comment_huel(request):
    """Add comment to a huel"""
    try:
        huel_id = request.data.get('huel_id')
        text = request.data.get('text')
        is_anonymous = request.data.get('is_anonymous', True)
        
        if not huel_id or not text:
            return Response({"error": "huel_id and text are required"}, status=400)
        
        huel = get_object_or_404(Huel, id=huel_id, is_active=True)
        
        comment = HuelComment.objects.create(
            user=request.user,
            huel=huel,
            text=text,
            is_anonymous=is_anonymous
        )
        
        return Response({
            "success": "Comment added successfully",
            "comment": HuelCommentSerializer(comment).data
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status=500)

# ========== DEPARTMENT/CLUB VIEWS ==========

@api_view(["GET"])
def department_clubs(request):
    """List departments and clubs with filtering"""
    club_type = request.GET.get('type')  # 'department' or 'club'
    category = request.GET.get('category')  # For filtering by category
    size = request.GET.get('size')  # For departments: 'major' or 'minor'
    
    items = DepartmentClub.objects.filter(is_active=True).prefetch_related('comments')
    
    if club_type:
        items = items.filter(type=club_type)
    
    if category:
        items = items.filter(category=category)
    
    if size:
        items = items.filter(size=size)
    
    # Order by vote count (highest first)
    items = items.order_by('-vote_count')
    
    serializer = DepartmentClubSerializer(items, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def vote_department_club(request):
    """Vote for a department or club"""
    try:
        item_id = request.data.get('item_id')
        if not item_id:
            return Response({"error": "item_id is required"}, status=400)
        
        item = get_object_or_404(DepartmentClub, id=item_id, is_active=True)
        
        # Check if user already voted
        existing_vote = DepartmentClubVote.objects.filter(
            user=request.user,
            department_club=item
        ).first()
        
        if existing_vote:
            return Response({
                "error": f"You have already voted for {item.name}"
            }, status=400)
        
        # Create vote
        DepartmentClubVote.objects.create(
            user=request.user,
            department_club=item
        )
        
        return Response({
            "success": f"Vote cast successfully for {item.name}",
            "item": DepartmentClubSerializer(item, context={'request': request}).data
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def comment_department_club(request):
    """Add comment to a department or club"""
    try:
        item_id = request.data.get('item_id')
        text = request.data.get('text')
        is_anonymous = request.data.get('is_anonymous', True)
        
        if not item_id or not text:
            return Response({"error": "item_id and text are required"}, status=400)
        
        item = get_object_or_404(DepartmentClub, id=item_id, is_active=True)
        
        comment = DepartmentClubComment.objects.create(
            user=request.user,
            department_club=item,
            text=text,
            is_anonymous=is_anonymous
        )
        
        return Response({
            "success": "Comment added successfully",
            "comment": DepartmentClubCommentSerializer(comment).data
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status=500)

# ========== STATISTICS VIEWS ==========

@api_view(["GET"])
def voting_stats(request):
    """Get comprehensive voting statistics"""
    try:
        stats = {
            'total_users': User.objects.count(),
            'election_votes': AnonymousElectionVote.objects.count(),
            'huel_ratings': HuelRating.objects.count(),
            'department_club_votes': DepartmentClubVote.objects.count(),
            'total_comments': HuelComment.objects.count() + DepartmentClubComment.objects.count(),
            'active_elections': ElectionPosition.objects.filter(is_active=True).count(),
            'active_huels': Huel.objects.filter(is_active=True).count(),
            'active_departments_clubs': DepartmentClub.objects.filter(is_active=True).count(),
        }
        
        serializer = VotingStatsSerializer(stats)
        return Response(serializer.data)
        
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(["GET"])
def dashboard_stats(request):
    """Get dashboard statistics for admin"""
    try:
        # Election stats
        election_stats = {}
        for position in ElectionPosition.objects.filter(is_active=True):
            total_votes = position.candidates.aggregate(total=Sum('vote_count'))['total'] or 0
            election_stats[position.name] = {
                'total_votes': total_votes,
                'candidates': position.candidates.filter(is_active=True).count()
            }
        
        # Top rated huels
        top_huels = Huel.objects.filter(is_active=True).order_by('-avg_overall')[:5]
        
        # Top departments/clubs
        top_departments = DepartmentClub.objects.filter(
            type='department', is_active=True
        ).order_by('-vote_count')[:5]
        
        top_clubs = DepartmentClub.objects.filter(
            type='club', is_active=True
        ).order_by('-vote_count')[:5]
        
        return Response({
            'election_stats': election_stats,
            'top_huels': HuelSerializer(top_huels, many=True).data,
            'top_departments': DepartmentClubSerializer(top_departments, many=True).data,
            'top_clubs': DepartmentClubSerializer(top_clubs, many=True).data,
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(["GET"])
def candidates_by_position(request):
    """Get election candidates grouped by position"""
    try:
        president_position = ElectionPosition.objects.filter(name="President", is_active=True).first()
        gensec_position = ElectionPosition.objects.filter(name="General Secretary", is_active=True).first()
        
        president_candidates = []
        gensec_candidates = []
        
        if president_position:
            president_candidates = ElectionCandidate.objects.filter(
                position=president_position, 
                is_active=True
            ).order_by('-vote_count')
            
        if gensec_position:
            gensec_candidates = ElectionCandidate.objects.filter(
                position=gensec_position, 
                is_active=True
            ).order_by('-vote_count')
        
        return Response({
            'president': ElectionCandidateSerializer(president_candidates, many=True).data,
            'gensec': ElectionCandidateSerializer(gensec_candidates, many=True).data
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(["GET"])
def election_live_stats(request):
    """Get live election statistics"""
    try:
        president_position = ElectionPosition.objects.filter(name="President", is_active=True).first()
        gensec_position = ElectionPosition.objects.filter(name="General Secretary", is_active=True).first()
        
        # Calculate total votes across all positions
        total_all_votes = AnonymousElectionVote.objects.count()
        
        stats = {
            'total_voters': User.objects.filter(is_active=True).count(),
            'total_votes_cast': total_all_votes,
            'president': {
                'total_votes': 0,
                'candidates': []
            },
            'gensec': {
                'total_votes': 0,
                'candidates': []
            }
        }
        
        if president_position:
            president_votes = AnonymousElectionVote.objects.filter(position=president_position).count()
            stats['president']['total_votes'] = president_votes
            
            candidates = ElectionCandidate.objects.filter(
                position=president_position, 
                is_active=True
            ).order_by('-vote_count')
            
            for candidate in candidates:
                stats['president']['candidates'].append({
                    'name': candidate.name,
                    'votes': candidate.vote_count,
                    'percentage': candidate.get_vote_percentage()
                })
        
        if gensec_position:
            gensec_votes = AnonymousElectionVote.objects.filter(position=gensec_position).count()
            stats['gensec']['total_votes'] = gensec_votes
            
            candidates = ElectionCandidate.objects.filter(
                position=gensec_position, 
                is_active=True
            ).order_by('-vote_count')
            
            for candidate in candidates:
                stats['gensec']['candidates'].append({
                    'name': candidate.name,
                    'votes': candidate.vote_count,
                    'percentage': candidate.get_vote_percentage()
                })
        
        return Response(stats)
        
    except Exception as e:
        return Response({"error": str(e)}, status=500)

