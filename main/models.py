from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import hashlib
import secrets

# ========== ELECTION MODELS ==========

class ElectionPosition(models.Model):
    name = models.CharField(max_length=100, unique=True)  # President, General Secretary, etc.
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ElectionCandidate(models.Model):
    name = models.CharField(max_length=100)
    position = models.ForeignKey(ElectionPosition, on_delete=models.CASCADE, related_name='candidates')
    party = models.CharField(max_length=100, blank=True)
    manifesto = models.TextField()
    agenda = models.JSONField(default=list)  # List of agenda items
    image = models.URLField(blank=True)
    vote_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['name', 'position']

    def __str__(self):
        return f"{self.name} - {self.position.name}"

    def get_vote_percentage(self):
        total_votes = ElectionCandidate.objects.filter(position=self.position).aggregate(
            total=models.Sum('vote_count'))['total'] or 0
        if total_votes == 0:
            return 0
        return round((self.vote_count / total_votes) * 100, 1)


class AnonymousElectionVote(models.Model):
    """
    Anonymous voting system where votes cannot be traced back to users.
    Uses cryptographic hashing to ensure one-vote-per-user while maintaining anonymity.
    """
    # Anonymous identifier - one-way hash of user ID + salt
    voter_hash = models.CharField(max_length=64, db_index=True)
    
    # Vote details
    candidate = models.ForeignKey(ElectionCandidate, on_delete=models.CASCADE, related_name='anonymous_votes')
    position = models.ForeignKey(ElectionPosition, on_delete=models.CASCADE)
    
    # Cryptographic verification (without revealing identity)
    vote_signature = models.CharField(max_length=128)  # Cryptographic signature for verification
    
    # Metadata
    voted_at = models.DateTimeField(auto_now_add=True)
    ip_hash = models.CharField(max_length=64, blank=True)  # Hashed IP for basic fraud prevention
    
    class Meta:
        unique_together = ['voter_hash', 'position']  # One vote per position per anonymous voter
        indexes = [
            models.Index(fields=['position', 'voted_at']),
            models.Index(fields=['candidate', 'voted_at']),
        ]

    @staticmethod
    def create_voter_hash(user_id, position_id):
        """Create anonymous voter hash from user ID and position"""
        # Use a secret salt stored in settings for additional security
        salt = "pollz_anonymous_voting_salt_2024"  # In production, this should be in settings
        data = f"{user_id}:{position_id}:{salt}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    @staticmethod
    def create_vote_signature(voter_hash, candidate_id, timestamp):
        """Create cryptographic signature for vote verification"""
        data = f"{voter_hash}:{candidate_id}:{timestamp}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    @staticmethod
    def hash_ip(ip_address):
        """Hash IP address for basic fraud prevention without storing actual IP"""
        if not ip_address:
            return ""
        salt = "pollz_ip_salt_2024"  # In production, this should be in settings
        data = f"{ip_address}:{salt}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    def __str__(self):
        return f"Anonymous vote for {self.candidate.name} in {self.position.name}"

# ========== HUEL (COURSE) MODELS ==========

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    short_name = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.short_name

class Huel(models.Model):
    code = models.CharField(max_length=20, unique=True)  # CS F211, MATH F111, etc.
    name = models.CharField(max_length=200)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='huels')
    instructor = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    # Aggregated ratings (calculated from individual ratings)
    avg_grading = models.FloatField(default=0.0)
    avg_toughness = models.FloatField(default=0.0)
    avg_overall = models.FloatField(default=0.0)
    
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

    def update_ratings(self):
        """Update aggregated ratings from individual ratings"""
        ratings = self.ratings.all()
        if ratings.exists():
            self.avg_grading = ratings.aggregate(avg=models.Avg('grading'))['avg'] or 0
            self.avg_toughness = ratings.aggregate(avg=models.Avg('toughness'))['avg'] or 0
            self.avg_overall = ratings.aggregate(avg=models.Avg('overall'))['avg'] or 0
        else:
            self.avg_grading = self.avg_toughness = self.avg_overall = 0
        self.save()

class HuelRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    huel = models.ForeignKey(Huel, on_delete=models.CASCADE, related_name='ratings')
    
    # Ratings (1-5 scale)
    grading = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    toughness = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    overall = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'huel']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.huel.update_ratings()

    def __str__(self):
        return f"{self.user.username} rated {self.huel.code}"


class HuelComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    huel = models.ForeignKey(Huel, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    is_anonymous = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment on {self.huel.code} by {self.user.username}"

# ========== DEPARTMENT/CLUB VOTING MODELS ==========

class DepartmentClub(models.Model):
    TYPE_CHOICES = [
        ('department', 'Department'),
        ('club', 'Club'),
    ]
    
    SIZE_CHOICES = [
        ('major', 'Major'),
        ('minor', 'Minor'),
    ]
    
    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=50, blank=True)  # Increased length for longer names
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    size = models.CharField(max_length=10, choices=SIZE_CHOICES, blank=True)  # Major/Minor for departments
    category = models.CharField(max_length=100, blank=True)  # Extended category field
    role = models.TextField(blank=True)  # Detailed role description
    description = models.TextField()
    
    # For departments: achievements, For clubs: activities
    highlights = models.JSONField(default=list)
    
    vote_count = models.IntegerField(default=0)
    image = models.URLField(blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['name', 'type']

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"

class DepartmentClubVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    department_club = models.ForeignKey(DepartmentClub, on_delete=models.CASCADE, related_name='votes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'department_club']


    def __str__(self):
        return f"{self.user.username} voted for {self.department_club.name}"

class DepartmentClubComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    department_club = models.ForeignKey(DepartmentClub, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    is_anonymous = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment on {self.department_club.name} by {self.user.username}"

# ========== USER PROFILE ==========

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    google_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    picture = models.URLField(blank=True)
    is_verified = models.BooleanField(default=False)
    
    # Voting status flags (boolean only, not who they voted for)
    voted_president = models.BooleanField(default=False)
    voted_gen_sec = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s profile"