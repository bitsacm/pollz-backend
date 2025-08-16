from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    ElectionPosition, ElectionCandidate, AnonymousElectionVote,
    Department, Huel, HuelRating, HuelComment,
    DepartmentClub, DepartmentClubVote, DepartmentClubComment,
    UserProfile
)

# ========== USER SERIALIZERS ==========

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['user', 'google_id', 'picture', 'is_verified', 'voted_president', 'voted_gen_sec', 'created_at']

# ========== ELECTION SERIALIZERS ==========

class ElectionPositionSerializer(serializers.ModelSerializer):
    candidate_count = serializers.SerializerMethodField()
    total_votes = serializers.SerializerMethodField()
    
    def get_candidate_count(self, obj):
        return obj.candidates.filter(is_active=True).count()
    
    def get_total_votes(self, obj):
        return obj.candidates.aggregate(total=serializers.models.Sum('vote_count'))['total'] or 0
    
    class Meta:
        model = ElectionPosition
        fields = ['id', 'name', 'description', 'is_active', 'candidate_count', 'total_votes', 'created_at']

class ElectionCandidateSerializer(serializers.ModelSerializer):
    position_name = serializers.CharField(source='position.name', read_only=True)
    vote_percentage = serializers.SerializerMethodField()
    user_has_voted = serializers.SerializerMethodField()
    
    def get_vote_percentage(self, obj):
        return obj.get_vote_percentage()
    
    def get_user_has_voted(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            # Check anonymous votes using voter hash
            voter_hash = AnonymousElectionVote.create_voter_hash(
                request.user.id, 
                obj.position.id
            )
            return AnonymousElectionVote.objects.filter(
                voter_hash=voter_hash, 
                position=obj.position
            ).exists()
        return False
    
    class Meta:
        model = ElectionCandidate
        fields = [
            'id', 'name', 'position', 'position_name', 'party', 'manifesto', 
            'agenda', 'image', 'vote_count', 'vote_percentage', 'user_has_voted',
            'is_active', 'created_at'
        ]


class AnonymousElectionVoteSerializer(serializers.ModelSerializer):
    """Serializer for anonymous votes - excludes sensitive data"""
    candidate_name = serializers.CharField(source='candidate.name', read_only=True)
    position_name = serializers.CharField(source='position.name', read_only=True)
    voter_id = serializers.SerializerMethodField()
    
    def get_voter_id(self, obj):
        """Return only first 8 characters of hash for identification"""
        return obj.voter_hash[:8]
    
    class Meta:
        model = AnonymousElectionVote
        fields = ['id', 'candidate', 'candidate_name', 'position', 'position_name', 'voter_id', 'voted_at']
        read_only_fields = ['voter_id', 'voted_at']

# ========== HUEL SERIALIZERS ==========

class DepartmentSerializer(serializers.ModelSerializer):
    huel_count = serializers.SerializerMethodField()
    
    def get_huel_count(self, obj):
        return obj.huels.filter(is_active=True).count()
    
    class Meta:
        model = Department
        fields = ['id', 'name', 'short_name', 'description', 'huel_count']

class HuelCommentSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    time_ago = serializers.SerializerMethodField()
    
    def get_user_name(self, obj):
        return 'Anonymous' if obj.is_anonymous else obj.user.get_full_name() or obj.user.username
    
    def get_time_ago(self, obj):
        from django.utils import timezone
        from datetime import timedelta
        
        now = timezone.now()
        diff = now - obj.created_at
        
        if diff.days > 0:
            return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        else:
            return "Just now"
    
    class Meta:
        model = HuelComment
        fields = ['id', 'text', 'user_name', 'time_ago', 'created_at']
        read_only_fields = ['created_at']

class HuelRatingSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = HuelRating
        fields = ['id', 'user_name', 'grading', 'toughness', 'overall', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class HuelSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.short_name', read_only=True)
    comments = HuelCommentSerializer(many=True, read_only=True)
    user_rating = serializers.SerializerMethodField()
    rating_count = serializers.SerializerMethodField()
    upvotes = serializers.SerializerMethodField()
    downvotes = serializers.SerializerMethodField()
    avg_grading = serializers.SerializerMethodField()
    avg_toughness = serializers.SerializerMethodField()
    avg_overall = serializers.SerializerMethodField()
    
    def get_user_rating(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                rating = obj.ratings.get(user=request.user)
                return HuelRatingSerializer(rating).data
            except HuelRating.DoesNotExist:
                return None
        return None
    
    
    def get_rating_count(self, obj):
        return obj.ratings.count()
    
    def get_upvotes(self, obj):
        # Upvotes removed - return 0
        return 0
    
    def get_downvotes(self, obj):
        # Downvotes removed - return 0
        return 0
    
    def get_avg_grading(self, obj):
        from django.db.models import Avg
        avg = obj.ratings.aggregate(avg=Avg('grading'))['avg']
        return avg if avg else 0.0
    
    def get_avg_toughness(self, obj):
        from django.db.models import Avg
        avg = obj.ratings.aggregate(avg=Avg('toughness'))['avg']
        return avg if avg else 0.0
    
    def get_avg_overall(self, obj):
        # Calculate overall as average of grading, toughness, and overall rating
        from django.db.models import Avg
        ratings = obj.ratings.aggregate(
            avg_grading=Avg('grading'),
            avg_toughness=Avg('toughness'),
            avg_overall=Avg('overall')
        )
        
        # If we have ratings, calculate the average of all three
        if ratings['avg_grading'] and ratings['avg_toughness'] and ratings['avg_overall']:
            return (ratings['avg_grading'] + ratings['avg_toughness'] + ratings['avg_overall']) / 3
        elif ratings['avg_overall']:
            return ratings['avg_overall']
        else:
            return 0.0
    
    class Meta:
        model = Huel
        fields = [
            'id', 'code', 'name', 'department', 'department_name', 'instructor',
            'description', 'avg_grading', 'avg_toughness', 'avg_overall',
            'upvotes', 'downvotes', 'rating_count', 'user_rating',
            'comments', 'is_active', 'created_at', 'updated_at'
        ]


# ========== DEPARTMENT/CLUB SERIALIZERS ==========

class DepartmentClubCommentSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    time_ago = serializers.SerializerMethodField()
    
    def get_user_name(self, obj):
        return 'Anonymous' if obj.is_anonymous else obj.user.get_full_name() or obj.user.username
    
    def get_time_ago(self, obj):
        from django.utils import timezone
        
        now = timezone.now()
        diff = now - obj.created_at
        
        if diff.days > 0:
            return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        else:
            return "Just now"
    
    class Meta:
        model = DepartmentClubComment
        fields = ['id', 'text', 'user_name', 'time_ago', 'created_at']
        read_only_fields = ['created_at']

class DepartmentClubSerializer(serializers.ModelSerializer):
    comments = DepartmentClubCommentSerializer(many=True, read_only=True)
    user_has_voted = serializers.SerializerMethodField()
    rank = serializers.SerializerMethodField()
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    size_display = serializers.CharField(source='get_size_display', read_only=True)
    vote_count = serializers.SerializerMethodField()
    
    def get_user_has_voted(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.votes.filter(user=request.user).exists()
        return False
    
    def get_vote_count(self, obj):
        # Return actual vote count from related votes
        return obj.votes.count()
    
    def get_rank(self, obj):
        # Calculate rank based on actual vote count within the same type and size
        from django.db.models import Count
        
        # Get all items of same type with their vote counts
        queryset = DepartmentClub.objects.filter(
            type=obj.type,
            is_active=True
        ).annotate(
            actual_vote_count=Count('votes')
        )
        
        if obj.size:
            queryset = queryset.filter(size=obj.size)
        
        # Get current item's vote count
        current_votes = obj.votes.count()
        
        # Count how many have more votes
        higher_vote_count = queryset.filter(
            actual_vote_count__gt=current_votes
        ).count()
        
        return higher_vote_count + 1
    
    class Meta:
        model = DepartmentClub
        fields = [
            'id', 'name', 'short_name', 'type', 'type_display', 'size', 'size_display', 
            'category', 'role', 'description', 'highlights', 'vote_count', 'image', 
            'user_has_voted', 'rank', 'comments', 'is_active', 'created_at'
        ]

class DepartmentClubVoteSerializer(serializers.ModelSerializer):
    department_club_name = serializers.CharField(source='department_club.name', read_only=True)
    
    class Meta:
        model = DepartmentClubVote
        fields = ['id', 'department_club', 'department_club_name', 'created_at']
        read_only_fields = ['created_at']

# ========== STATISTICS SERIALIZERS ==========

class VotingStatsSerializer(serializers.Serializer):
    """Serializer for voting statistics across all platforms"""
    total_users = serializers.IntegerField()
    election_votes = serializers.IntegerField()
    huel_ratings = serializers.IntegerField()
    department_club_votes = serializers.IntegerField()
    total_comments = serializers.IntegerField()
    active_elections = serializers.IntegerField()
    active_huels = serializers.IntegerField()
    active_departments_clubs = serializers.IntegerField()