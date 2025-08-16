from django.urls import path
from . import views

urlpatterns = [
    # ========== AUTHENTICATION ==========
    path('auth/google-login/', views.google_login, name='google_login'),
    path('auth/logout/', views.logout, name='logout'),
    path('auth/profile/', views.user_profile, name='user_profile'),
    
    # ========== ELECTIONS ==========
    path('elections/positions/', views.election_positions, name='election_positions'),
    path('elections/candidates/', views.election_candidates, name='election_candidates'),
    path('elections/candidates-by-position/', views.candidates_by_position, name='candidates_by_position'),
    path('elections/live-stats/', views.election_live_stats, name='election_live_stats'),
    path('elections/cast-anonymous-vote/', views.cast_anonymous_election_vote, name='cast_anonymous_election_vote'),
    path('elections/check-vote-status/', views.check_anonymous_vote_status, name='check_anonymous_vote_status'),
    
    # ========== HUELS (COURSES) ==========
    path('huels/departments/', views.departments, name='departments'),
    path('huels/', views.huels, name='huels'),
    path('huels/<int:huel_id>/', views.huel_detail, name='huel_detail'),
    path('huels/rate/', views.rate_huel, name='rate_huel'),
    path('huels/comment/', views.comment_huel, name='comment_huel'),
    
    # ========== DEPARTMENTS/CLUBS ==========
    path('departments-clubs/', views.department_clubs, name='department_clubs'),
    path('departments-clubs/vote/', views.vote_department_club, name='vote_department_club'),
    path('departments-clubs/comment/', views.comment_department_club, name='comment_department_club'),
    
    # ========== STATISTICS ==========
    path('stats/', views.voting_stats, name='voting_stats'),
    path('stats/dashboard/', views.dashboard_stats, name='dashboard_stats'),
    
    # ========== LEGACY ENDPOINTS (for backward compatibility) ==========
    path('gensec_vote/', views.cast_anonymous_election_vote, name='gensec_vote_legacy'),  # Redirect to anonymous voting
    path('prez_vote/', views.cast_anonymous_election_vote, name='prez_vote_legacy'),     # Redirect to anonymous voting
    path('candidate-data/', views.election_candidates, name='candidate_data_legacy'),
    path('total-votes/', views.voting_stats, name='total_votes_legacy'),
]