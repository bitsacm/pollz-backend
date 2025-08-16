from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from main.models import (
    ElectionPosition, ElectionCandidate, ElectionVote,
    Department, Huel, HuelRating, HuelVote, HuelComment,
    DepartmentClub, DepartmentClubVote, DepartmentClubComment,
    UserProfile
)

class Command(BaseCommand):
    help = 'Populate database with sample data for testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create sample users
        self.create_sample_users()
        
        # Create sample departments and huels
        self.create_sample_huels()
        
        # Create sample elections
        self.create_sample_elections()
        
        # Create sample departments/clubs
        self.create_sample_department_clubs()
        
        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
    
    def create_sample_users(self):
        """Create sample users for testing"""
        sample_users = [
            {'username': 'testuser1', 'email': 'test1@bits-pilani.ac.in', 'first_name': 'John', 'last_name': 'Doe'},
            {'username': 'testuser2', 'email': 'test2@bits-pilani.ac.in', 'first_name': 'Jane', 'last_name': 'Smith'},
            {'username': 'testuser3', 'email': 'test3@bits-pilani.ac.in', 'first_name': 'Bob', 'last_name': 'Wilson'},
        ]
        
        for user_data in sample_users:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                }
            )
            if created:
                # Create user profile
                UserProfile.objects.get_or_create(
                    user=user,
                    defaults={'is_verified': True}
                )
                self.stdout.write(f'Created user: {user.username}')
    
    def create_sample_huels(self):
        """Create sample departments and huels"""
        # Create departments
        departments_data = [
            {'name': 'Computer Science', 'short_name': 'CS'},
            {'name': 'Mathematics', 'short_name': 'MATH'},
            {'name': 'Physics', 'short_name': 'PHY'},
            {'name': 'Electrical and Electronics', 'short_name': 'EEE'},
            {'name': 'Mechanical Engineering', 'short_name': 'MECH'},
        ]
        
        departments = {}
        for dept_data in departments_data:
            dept, created = Department.objects.get_or_create(
                short_name=dept_data['short_name'],
                defaults={'name': dept_data['name']}
            )
            departments[dept_data['short_name']] = dept
            if created:
                self.stdout.write(f'Created department: {dept.short_name}')
        
        # Create huels
        huels_data = [
            {
                'code': 'CS F211',
                'name': 'Data Structures and Algorithms',
                'department': 'CS',
                'instructor': 'Dr. Sharma',
                'description': 'Fundamental data structures and algorithms',
                'avg_grading': 0.0,
                'avg_toughness': 0.0,
                'avg_overall': 0.0,
                'upvotes': 0,
                'downvotes': 0,
            },
            {
                'code': 'MATH F111',
                'name': 'Mathematics I',
                'department': 'MATH',
                'instructor': 'Prof. Kumar',
                'description': 'Calculus and linear algebra',
                'avg_grading': 0.0,
                'avg_toughness': 0.0,
                'avg_overall': 0.0,
                'upvotes': 0,
                'downvotes': 0,
            },
            {
                'code': 'PHY F111',
                'name': 'Mechanics, Oscillations and Waves',
                'department': 'PHY',
                'instructor': 'Dr. Gupta',
                'description': 'Classical mechanics and wave physics',
                'avg_grading': 0.0,
                'avg_toughness': 0.0,
                'avg_overall': 0.0,
                'upvotes': 0,
                'downvotes': 0,
            },
            {
                'code': 'EEE F111',
                'name': 'Electrical Sciences',
                'department': 'EEE',
                'instructor': 'Prof. Singh',
                'description': 'Basic electrical engineering concepts',
                'avg_grading': 0.0,
                'avg_toughness': 0.0,
                'avg_overall': 0.0,
                'upvotes': 0,
                'downvotes': 0,
            },
            {
                'code': 'CS F213',
                'name': 'Object Oriented Programming',
                'department': 'CS',
                'instructor': 'Dr. Patel',
                'description': 'Java programming and OOP concepts',
                'avg_grading': 0.0,
                'avg_toughness': 0.0,
                'avg_overall': 0.0,
                'upvotes': 0,
                'downvotes': 0,
            },
        ]
        
        for huel_data in huels_data:
            huel, created = Huel.objects.get_or_create(
                code=huel_data['code'],
                defaults={
                    'name': huel_data['name'],
                    'department': departments[huel_data['department']],
                    'instructor': huel_data['instructor'],
                    'description': huel_data['description'],
                    'avg_grading': huel_data['avg_grading'],
                    'avg_toughness': huel_data['avg_toughness'],
                    'avg_overall': huel_data['avg_overall'],
                    'upvotes': huel_data['upvotes'],
                    'downvotes': huel_data['downvotes'],
                }
            )
            if created:
                self.stdout.write(f'Created huel: {huel.code}')
    
    def create_sample_elections(self):
        """Create sample election data"""
        # Create positions
        positions_data = [
            {'name': 'President', 'description': 'Student Union President'},
            {'name': 'General Secretary', 'description': 'Student Union General Secretary'},
            {'name': 'Sports Secretary', 'description': 'Student Union Sports Secretary'},
        ]
        
        positions = {}
        for pos_data in positions_data:
            pos, created = ElectionPosition.objects.get_or_create(
                name=pos_data['name'],
                defaults={'description': pos_data['description']}
            )
            positions[pos_data['name']] = pos
            if created:
                self.stdout.write(f'Created position: {pos.name}')
        
        # Create candidates
        candidates_data = [
            {
                'name': 'Ahaan Khurana',
                'position': 'President',
                'party': 'Progressive Alliance',
                'manifesto': 'Working towards better infrastructure and student facilities.',
                'agenda': ['Better hostel facilities', 'Improved mess food', 'More recreational activities'],
                'vote_count': 0,
            },
            {
                'name': 'Rival Candidate',
                'position': 'President',
                'party': 'Student First',
                'manifesto': 'Focusing on academic excellence and career development.',
                'agenda': ['Better placement support', 'More industry connections', 'Academic reforms'],
                'vote_count': 0,
            },
            {
                'name': 'Sarah Johnson',
                'position': 'General Secretary',
                'party': 'Progressive Alliance',
                'manifesto': 'Enhancing student experience and campus life.',
                'agenda': ['More student events', 'Better communication', 'Student welfare'],
                'vote_count': 0,
            },
        ]
        
        for cand_data in candidates_data:
            cand, created = ElectionCandidate.objects.get_or_create(
                name=cand_data['name'],
                position=positions[cand_data['position']],
                defaults={
                    'party': cand_data['party'],
                    'manifesto': cand_data['manifesto'],
                    'agenda': cand_data['agenda'],
                    'vote_count': cand_data['vote_count'],
                }
            )
            if created:
                self.stdout.write(f'Created candidate: {cand.name}')
    
    def create_sample_department_clubs(self):
        """Create sample departments and clubs"""
        items_data = [
            {
                'name': 'Computer Science Department',
                'short_name': 'CS Dept',
                'type': 'department',
                'description': 'Department of Computer Science and Information Systems',
                'highlights': ['AI Research', 'Competitive Programming', 'Industry Collaborations'],
                'vote_count': 0,
            },
            {
                'name': 'Association for Computing Machinery',
                'short_name': 'ACM',
                'type': 'club',
                'category': 'Technical',
                'description': 'Premier computer science club promoting coding and technology.',
                'highlights': ['Coding Competitions', 'Tech Talks', 'Workshops'],
                'vote_count': 0,
            },
            {
                'name': 'Department of Electronic and Electrical Engineering',
                'short_name': 'EEE Dept',
                'type': 'department',
                'description': 'Department focusing on electronics and electrical systems',
                'highlights': ['Circuit Design', 'Power Systems', 'Embedded Systems'],
                'vote_count': 0,
            },
            {
                'name': 'Music Society',
                'short_name': 'Music Club',
                'type': 'club',
                'category': 'Cultural',
                'description': 'Promoting musical talent and organizing cultural events.',
                'highlights': ['Live Performances', 'Music Festivals', 'Talent Shows'],
                'vote_count': 0,
            },
            {
                'name': 'Robotics Club',
                'short_name': 'Robotics',
                'type': 'club',
                'category': 'Technical',
                'description': 'Building and programming robots for competitions.',
                'highlights': ['Robot Wars', 'Automation Projects', 'AI Integration'],
                'vote_count': 0,
            },
        ]
        
        for item_data in items_data:
            item, created = DepartmentClub.objects.get_or_create(
                name=item_data['name'],
                type=item_data['type'],
                defaults={
                    'short_name': item_data['short_name'],
                    'category': item_data.get('category', ''),
                    'description': item_data['description'],
                    'highlights': item_data['highlights'],
                    'vote_count': item_data['vote_count'],
                }
            )
            if created:
                self.stdout.write(f'Created {item.get_type_display()}: {item.name}')