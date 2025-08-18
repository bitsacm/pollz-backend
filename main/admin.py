from django.contrib import admin
from django.utils.html import format_html
from .models import (
    VotingSession, ElectionPosition, ElectionCandidate, AnonymousElectionVote,
    Department, Huel, HuelRating, HuelComment,
    DepartmentClub, DepartmentClubVote, DepartmentClubComment,
    UserProfile
)

# ========== VOTING CONTROL ADMIN ==========

@admin.register(VotingSession)
class VotingSessionAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'voting_type', 'status_display', 'is_active', 
        'voting_start_time', 'voting_end_time', 'created_at'
    ]
    list_filter = ['voting_type', 'is_active', 'created_at']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at', 'created_by']
    
    fieldsets = [
        ('Basic Information', {
            'fields': ['name', 'voting_type', 'is_active']
        }),
        ('Time Control', {
            'fields': ['voting_start_time', 'voting_end_time'],
            'description': 'Leave empty for manual control via "is_active" toggle'
        }),
        ('User Messages', {
            'fields': [
                'message_during_voting', 'message_before_start', 
                'message_after_end', 'message_inactive'
            ],
            'classes': ['collapse']
        }),
        ('Metadata', {
            'fields': ['created_at', 'updated_at', 'created_by'],
            'classes': ['collapse']
        })
    ]
    
    actions = ['activate_voting', 'deactivate_voting']
    
    def status_display(self, obj):
        status, message = obj.get_current_status()
        colors = {
            'active': 'green',
            'not_started': 'orange', 
            'ended': 'red',
            'inactive': 'gray'
        }
        return format_html(
            '<span style="color: {};">{}</span>',
            colors.get(status, 'black'),
            status.title().replace('_', ' ')
        )
    status_display.short_description = 'Current Status'
    
    def activate_voting(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} voting session(s) activated.')
    activate_voting.short_description = 'Activate selected voting sessions'
    
    def deactivate_voting(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} voting session(s) deactivated.')
    deactivate_voting.short_description = 'Deactivate selected voting sessions'
    
    def save_model(self, request, obj, form, change):
        if not change:  # Only set created_by for new objects
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

# ========== USER PROFILE ADMIN ==========

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user_username', 'user_email', 'is_verified', 'created_at']
    list_filter = ['is_verified', 'created_at']
    search_fields = ['user__username', 'user__email', 'google_id']
    readonly_fields = ['created_at']
    
    def user_username(self, obj):
        return obj.user.username
    user_username.short_description = 'Username'
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'

# ========== ELECTION ADMIN ==========

@admin.register(ElectionPosition)
class ElectionPositionAdmin(admin.ModelAdmin):
    list_display = ['name', 'candidate_count', 'total_votes', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name']
    readonly_fields = ['created_at']
    
    def candidate_count(self, obj):
        return obj.candidates.filter(is_active=True).count()
    candidate_count.short_description = 'Active Candidates'
    
    def total_votes(self, obj):
        return sum(candidate.vote_count for candidate in obj.candidates.all())
    total_votes.short_description = 'Total Votes'

@admin.register(ElectionCandidate)
class ElectionCandidateAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'party', 'vote_count', 'vote_percentage', 'is_active']
    list_filter = ['position', 'party', 'is_active', 'created_at']
    search_fields = ['name', 'party']
    readonly_fields = ['vote_count', 'created_at']
    fields = [
        'name', 'position', 'party', 'manifesto', 'agenda', 
        'image', 'vote_count', 'is_active', 'created_at'
    ]
    
    def vote_percentage(self, obj):
        return f"{obj.get_vote_percentage()}%"
    vote_percentage.short_description = 'Vote %'


@admin.register(AnonymousElectionVote)
class AnonymousElectionVoteAdmin(admin.ModelAdmin):
    list_display = ['voter_hash_short', 'candidate', 'position', 'voted_at', 'signature_valid']
    list_filter = ['position', 'voted_at']
    search_fields = ['candidate__name']
    readonly_fields = ['voter_hash', 'vote_signature', 'voted_at', 'ip_hash']
    
    def voter_hash_short(self, obj):
        """Show only first 8 characters of hash for privacy"""
        return f"{obj.voter_hash[:8]}..."
    voter_hash_short.short_description = 'Voter ID'
    
    def signature_valid(self, obj):
        """Verify vote signature integrity"""
        expected_signature = AnonymousElectionVote.create_vote_signature(
            obj.voter_hash, 
            obj.candidate.id, 
            obj.voted_at.isoformat()
        )
        is_valid = obj.vote_signature == expected_signature
        color = 'green' if is_valid else 'red'
        return format_html(
            '<span style="color: {};">{}</span>',
            color, '✓ Valid' if is_valid else '✗ Invalid'
        )
    signature_valid.short_description = 'Signature'
    
    def has_change_permission(self, request, obj=None):
        """Prevent modification of anonymous votes to maintain integrity"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of anonymous votes to maintain audit trail"""
        return False

# ========== HUEL ADMIN ==========

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['short_name', 'name', 'huel_count']
    search_fields = ['name', 'short_name']
    
    def huel_count(self, obj):
        return obj.huels.filter(is_active=True).count()
    huel_count.short_description = 'Active Huels'

@admin.register(Huel)
class HuelAdmin(admin.ModelAdmin):
    list_display = [
        'code', 'name', 'department', 'instructor', 
        'avg_overall_display', 'rating_count', 'is_active'
    ]
    list_filter = ['department', 'is_active', 'created_at']
    search_fields = ['code', 'name', 'instructor']
    readonly_fields = [
        'avg_grading', 'avg_toughness', 'avg_overall', 
        'created_at', 'updated_at'
    ]
    fields = [
        'code', 'name', 'department', 'instructor', 'description',
        'avg_grading', 'avg_toughness', 'avg_overall',
        'is_active', 'created_at', 'updated_at'
    ]
    
    def avg_overall_display(self, obj):
        if obj.avg_overall >= 4.0:
            color = 'green'
        elif obj.avg_overall >= 3.5:
            color = 'orange'
        else:
            color = 'red'
        return format_html(
            '<span style="color: {};">{}/5</span>',
            color, f'{obj.avg_overall:.1f}'
        )
    avg_overall_display.short_description = 'Overall Rating'
    
    def rating_count(self, obj):
        return obj.ratings.count()
    rating_count.short_description = 'Ratings'
    

@admin.register(HuelRating)
class HuelRatingAdmin(admin.ModelAdmin):
    list_display = ['user_email', 'huel_code', 'grading', 'toughness', 'overall', 'created_at']
    list_filter = ['huel__department', 'created_at']
    search_fields = ['user__email', 'huel__code', 'huel__name']
    readonly_fields = ['created_at', 'updated_at']
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User Email'
    
    def huel_code(self, obj):
        return obj.huel.code
    huel_code.short_description = 'Course Code'


@admin.register(HuelComment)
class HuelCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'huel_code', 'comment_preview', 'is_anonymous', 'created_at']
    list_filter = ['is_anonymous', 'created_at']
    search_fields = ['user__username', 'huel__code', 'text']
    readonly_fields = ['created_at']
    
    def huel_code(self, obj):
        return obj.huel.code
    huel_code.short_description = 'Course Code'
    
    def comment_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    comment_preview.short_description = 'Comment'

# ========== DEPARTMENT/CLUB ADMIN ==========

@admin.register(DepartmentClub)
class DepartmentClubAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'short_name', 'type', 'size', 'category', 
        'vote_count', 'rank_display', 'is_active'
    ]
    list_filter = ['type', 'size', 'category', 'is_active', 'created_at']
    search_fields = ['name', 'short_name', 'category', 'role']
    readonly_fields = ['vote_count', 'created_at']
    fieldsets = [
        ('Basic Information', {
            'fields': ['name', 'short_name', 'type', 'size', 'category']
        }),
        ('Description', {
            'fields': ['role', 'description', 'highlights']
        }),
        ('Statistics', {
            'fields': ['vote_count', 'is_active', 'created_at']
        }),
        ('Media', {
            'fields': ['image'],
            'classes': ['collapse']
        })
    ]
    
    def rank_display(self, obj):
        # Calculate rank within type and size
        filters = {
            'type': obj.type,
            'vote_count__gt': obj.vote_count,
            'is_active': True
        }
        if obj.size:
            filters['size'] = obj.size
            
        higher_count = DepartmentClub.objects.filter(**filters).count()
        rank = higher_count + 1
        
        if rank <= 3:
            color = 'gold' if rank == 1 else 'silver' if rank == 2 else '#CD7F32'
            return format_html(
                '<span style="color: {}; font-weight: bold;">#{}</span>',
                color, rank
            )
        return f"#{rank}"
    rank_display.short_description = 'Rank'

@admin.register(DepartmentClubVote)
class DepartmentClubVoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'department_club', 'department_club_type', 'created_at']
    list_filter = ['department_club__type', 'created_at']
    search_fields = ['user__username', 'department_club__name']
    readonly_fields = ['created_at']
    
    def department_club_type(self, obj):
        return obj.department_club.get_type_display()
    department_club_type.short_description = 'Type'

@admin.register(DepartmentClubComment)
class DepartmentClubCommentAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'department_club', 'comment_preview', 'is_anonymous', 'created_at'
    ]
    list_filter = ['is_anonymous', 'department_club__type', 'created_at']
    search_fields = ['user__username', 'department_club__name', 'text']
    readonly_fields = ['created_at']
    
    def comment_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    comment_preview.short_description = 'Comment'

# ========== ADMIN SITE CUSTOMIZATION ==========

admin.site.site_header = "Pollz Administration"
admin.site.site_title = "Pollz Admin"
admin.site.index_title = "Welcome to Pollz Administration Portal"