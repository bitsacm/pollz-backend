from django.core.management.base import BaseCommand
from main.models import DepartmentClub

class Command(BaseCommand):
    help = 'Populate database with complete OASIS clubs and departments structure'

    def handle(self, *args, **options):
        self.stdout.write('Creating OASIS clubs and departments data...')
        
        # First, remove existing club/department data if any
        DepartmentClub.objects.all().delete()
        self.stdout.write('Cleared existing club/department data')
        
        # MAJOR DEPARTMENTS (Headed by StuCCAns)
        major_departments = [
            {
                'name': 'Art, Design, and Publicity',
                'short_name': 'ADP',
                'type': 'department',
                'size': 'major',
                'category': 'Creative & Marketing',
                'role': 'Handles all design work including logos, posters, campus decorations, social media management, and on-campus publicity',
                'description': 'The creative powerhouse of OASIS, responsible for all visual communication and marketing materials',
                'highlights': [
                    'Design work including logos and posters',
                    'Campus decorations and aesthetics',
                    'Social media management',
                    'On-campus publicity coordination'
                ],
            },
            {
                'name': 'Controls',
                'short_name': 'CTRL',
                'type': 'department',
                'size': 'major',
                'category': 'Operations & Logistics',
                'role': 'Manages event registration, judge coordination, venue allocation, prize distribution, certificates, transportation, and overall event logistics',
                'description': 'The operational backbone ensuring smooth execution of all festival activities',
                'highlights': [
                    'Event registration management',
                    'Judge coordination',
                    'Venue allocation',
                    'Prize distribution and certificates',
                    'Transportation logistics'
                ],
            },
            {
                'name': 'Reception and Accommodation',
                'short_name': 'RecNAcc',
                'type': 'department',
                'size': 'major',
                'category': 'Hospitality & Guest Services',
                'role': 'Responsible for outstation participant reception, accommodation, hospitality, and protocol management',
                'description': 'Ensures comfortable stay and warm welcome for all outstation participants',
                'highlights': [
                    'Outstation participant reception',
                    'Accommodation arrangements',
                    'Hospitality services',
                    'Protocol management'
                ],
            },
            {
                'name': 'Sponsorship and Marketing',
                'short_name': 'SponsNMark',
                'type': 'department',
                'size': 'major',
                'category': 'Finance & Partnerships',
                'role': 'Handles all sponsorship activities, marketing partnerships, stall placements, and alumni relations',
                'description': 'Builds strategic partnerships and manages financial support for the festival',
                'highlights': [
                    'Sponsorship acquisition',
                    'Marketing partnerships',
                    'Stall placement coordination',
                    'Alumni relations'
                ],
            },
            {
                'name': 'Publications and Correspondence',
                'short_name': 'PubNCorr',
                'type': 'department',
                'size': 'major',
                'category': 'Communications & Documentation',
                'role': 'Manages all printing, correspondence with colleges, pre-invites, certificates, and official documentation',
                'description': 'Handles all official communication and documentation for the festival',
                'highlights': [
                    'Official printing and documentation',
                    'Inter-college correspondence',
                    'Pre-invitation management',
                    'Certificate preparation'
                ],
            },
            {
                'name': 'Visual Media',
                'short_name': 'VisMedia',
                'type': 'department',
                'size': 'major',
                'category': 'Digital Media & Technology',
                'role': 'Handles website development, live event coverage, promotional videos, and auditorium console management',
                'description': 'Manages all digital media and technological requirements for the festival',
                'highlights': [
                    'Website development and maintenance',
                    'Live event coverage',
                    'Promotional video production',
                    'Auditorium console management'
                ],
            },
            {
                'name': 'Finance',
                'short_name': 'Finance',
                'type': 'department',
                'size': 'major',
                'category': 'Finance & Administration',
                'role': 'Manages all financial aspects including budgets, tenders, bill clearance, and liaison with institute authorities',
                'description': 'Oversees all financial operations and administrative coordination (Position held by Students\' Union President)',
                'highlights': [
                    'Budget management and allocation',
                    'Tender processes',
                    'Bill clearance procedures',
                    'Institute authority liaison'
                ],
            },
            {
                'name': 'Inventory',
                'short_name': 'Inventory',
                'type': 'department',
                'size': 'major',
                'category': 'Operations & Supply Chain',
                'role': 'Handles inventory control, refreshment coupons, and assists Financial StuCCAn',
                'description': 'Manages all inventory and supply chain operations (Position held by General Secretary)',
                'highlights': [
                    'Inventory control and tracking',
                    'Refreshment coupon management',
                    'Supply chain coordination',
                    'Financial department assistance'
                ],
            },
        ]
        
        # MINOR DEPARTMENTS (Headed by Coordinators)
        minor_departments = [
            {
                'name': 'Audi Force',
                'short_name': 'AudiForce',
                'type': 'department',
                'size': 'minor',
                'category': 'Security & Crowd Management',
                'role': 'Provides security arrangements for auditorium events, manages ticketing, and controls auditorium access',
                'description': 'Ensures security and crowd management for all auditorium events',
                'highlights': [
                    'Auditorium security arrangements',
                    'Ticketing management',
                    'Access control',
                    'Crowd management'
                ],
            },
            {
                'name': 'Firewallz',
                'short_name': 'Firewallz',
                'type': 'department',
                'size': 'minor',
                'category': 'Security & Safety',
                'role': 'Handles campus-wide security, night patrolling, discipline enforcement, and participant verification',
                'description': 'Provides comprehensive security coverage across the entire campus',
                'highlights': [
                    'Campus-wide security',
                    'Night patrolling',
                    'Discipline enforcement',
                    'Participant verification'
                ],
            },
            {
                'name': 'Informalz',
                'short_name': 'Informalz',
                'type': 'department',
                'size': 'minor',
                'category': 'Entertainment & Activities',
                'role': 'Organizes informal events like treasure hunts and MAMO during the festival',
                'description': 'Creates fun and engaging informal activities for festival participants',
                'highlights': [
                    'Treasure hunt organization',
                    'MAMO event coordination',
                    'Informal activity planning',
                    'Entertainment programming'
                ],
            },
            {
                'name': 'Lights',
                'short_name': 'Lights',
                'type': 'department',
                'size': 'minor',
                'category': 'Technical Support',
                'role': 'Provides all lighting requirements at all venues during the festival',
                'description': 'Ensures proper lighting setup for all festival venues and events',
                'highlights': [
                    'Venue lighting setup',
                    'Event lighting coordination',
                    'Technical lighting support',
                    'Equipment maintenance'
                ],
            },
            {
                'name': 'Photography',
                'short_name': 'Photo',
                'type': 'department',
                'size': 'minor',
                'category': 'Media & Documentation',
                'role': 'Handles all photography work including pre-fest, fest coverage, and post-fest documentation',
                'description': 'Captures and documents all festival moments through professional photography',
                'highlights': [
                    'Pre-festival photography',
                    'Live event coverage',
                    'Post-festival documentation',
                    'Professional photo editing'
                ],
            },
            {
                'name': 'Sounds',
                'short_name': 'Sounds',
                'type': 'department',
                'size': 'minor',
                'category': 'Technical Support',
                'role': 'Provides all audio requirements and sound systems at all venues',
                'description': 'Manages audio systems and sound requirements for all festival events',
                'highlights': [
                    'Audio system setup',
                    'Sound quality management',
                    'Venue audio coordination',
                    'Technical sound support'
                ],
            },
            {
                'name': 'Stage Controls',
                'short_name': 'StageCtrl',
                'type': 'department',
                'size': 'minor',
                'category': 'Technical Support & Operations',
                'role': 'Manages stage requirements for auditorium events, inauguration ceremony, and auditorium cleanliness',
                'description': 'Oversees all stage-related operations and auditorium management',
                'highlights': [
                    'Stage setup and management',
                    'Auditorium event coordination',
                    'Inauguration ceremony support',
                    'Venue cleanliness maintenance'
                ],
            },
            {
                'name': 'Theatre',
                'short_name': 'Theatre',
                'type': 'department',
                'size': 'minor',
                'category': 'Performance Arts',
                'role': 'Conducts theatre events, choreography, fashion parade, and dance workshops',
                'description': 'Organizes and manages all theatrical and performance art events',
                'highlights': [
                    'Theatre event production',
                    'Choreography coordination',
                    'Fashion parade organization',
                    'Dance workshop facilitation'
                ],
            },
        ]
        
        # CLUBS (Headed by Coordinators/Secretaries)
        clubs = [
            # Cultural & Literary Clubs
            {
                'name': 'Oasis English Press',
                'short_name': 'OEP',
                'type': 'club',
                'category': 'Media & Journalism',
                'role': 'Handles all English press coverage, newsletters, wall magazines, and daily press publications',
                'description': 'The premier English journalism club covering all festival activities',
                'highlights': [
                    'English press coverage',
                    'Newsletter publication',
                    'Wall magazine creation',
                    'Daily press releases'
                ],
            },
            {
                'name': 'Oasis Hindi Press',
                'short_name': 'OHP',
                'type': 'club',
                'category': 'Media & Journalism',
                'role': 'Manages Hindi press coverage, newsletters, wall magazines, and daily Hindi publications',
                'description': 'Dedicated to Hindi journalism and regional language coverage',
                'highlights': [
                    'Hindi press coverage',
                    'Hindi newsletter publication',
                    'Regional wall magazines',
                    'Daily Hindi publications'
                ],
            },
            {
                'name': 'ELAS',
                'short_name': 'ELAS',
                'type': 'club',
                'category': 'Literary & Academic',
                'role': 'Conducts English language events like quizzes, crosswords, and literary activities',
                'description': 'English Language Activities Society promoting literary excellence',
                'highlights': [
                    'English quizzes and competitions',
                    'Crossword puzzles',
                    'Literary event organization',
                    'Language skill development'
                ],
            },
            {
                'name': 'HAS',
                'short_name': 'HAS',
                'type': 'club',
                'category': 'Literary & Academic',
                'role': 'Organizes Hindi language events including quizzes, debates, and crosswords',
                'description': 'Hindi Activities Society celebrating Hindi literature and culture',
                'highlights': [
                    'Hindi quizzes and debates',
                    'Hindi crosswords',
                    'Cultural literary events',
                    'Hindi language promotion'
                ],
            },
            {
                'name': 'Debating Society',
                'short_name': 'DebSoc',
                'type': 'club',
                'category': 'Literary & Oratory',
                'role': 'Conducts oratory and debating events in English',
                'description': 'Premier platform for debate and public speaking excellence',
                'highlights': [
                    'Debate competitions',
                    'Oratory events',
                    'Public speaking workshops',
                    'Parliamentary debates'
                ],
            },
            {
                'name': 'Poetry Club',
                'short_name': 'Poetry',
                'type': 'club',
                'category': 'Literary Arts',
                'role': 'Solely responsible for conducting the Purple Prose poetry event',
                'description': 'Dedicated to poetry and creative writing expression',
                'highlights': [
                    'Purple Prose poetry event',
                    'Poetry competitions',
                    'Creative writing workshops',
                    'Literary expression platforms'
                ],
            },
            
            # Performance Arts Clubs
            {
                'name': 'ARBITS',
                'short_name': 'ARBITS',
                'type': 'club',
                'category': 'Music & Entertainment',
                'role': 'Organizes professional shows and music events, handles artist coordination',
                'description': 'Association of Rock Music in BITS - the ultimate music experience',
                'highlights': [
                    'Professional show organization',
                    'Artist coordination',
                    'Music event management',
                    'Concert production'
                ],
            },
            {
                'name': 'Music Club',
                'short_name': 'Music',
                'type': 'club',
                'category': 'Music & Performance',
                'role': 'Conducts music events and competitions during the festival',
                'description': 'Celebrating musical talent and organizing diverse music competitions',
                'highlights': [
                    'Music competitions',
                    'Performance events',
                    'Talent showcases',
                    'Musical workshops'
                ],
            },
            {
                'name': 'Dance Club',
                'short_name': 'Dance',
                'type': 'club',
                'category': 'Dance & Performance',
                'role': 'Stages dance productions (competitive and non-competitive) during the festival',
                'description': 'Premier dance club showcasing various dance forms and cultures',
                'highlights': [
                    'Competitive dance events',
                    'Non-competitive productions',
                    'Dance workshops',
                    'Cultural dance showcases'
                ],
            },
            {
                'name': 'Mime',
                'short_name': 'Mime',
                'type': 'club',
                'category': 'Performance Arts',
                'role': 'Organizes mime and silent performance events',
                'description': 'Unique platform for silent art and expressive performance',
                'highlights': [
                    'Mime competitions',
                    'Silent performance events',
                    'Expression workshops',
                    'Non-verbal art promotion'
                ],
            },
            {
                'name': 'Karaoke Club',
                'short_name': 'Karaoke',
                'type': 'club',
                'category': 'Music & Entertainment',
                'role': 'Solely responsible for conducting "Scontro" karaoke events',
                'description': 'Fun and engaging karaoke experiences for all participants',
                'highlights': [
                    'Scontro karaoke events',
                    'Musical entertainment',
                    'Singing competitions',
                    'Interactive music sessions'
                ],
            },
            
            # Creative & Technical Clubs
            {
                'name': 'CrAC',
                'short_name': 'CrAC',
                'type': 'club',
                'category': 'Visual Arts & Creativity',
                'role': 'Conducts all fine arts related activities and competitions',
                'description': 'Creative Activities Club fostering artistic expression and creativity',
                'highlights': [
                    'Fine arts competitions',
                    'Creative workshops',
                    'Art exhibitions',
                    'Artistic skill development'
                ],
            },
            {
                'name': 'Photography Club',
                'short_name': 'PhotoClub',
                'type': 'club',
                'category': 'Media & Documentation',
                'role': 'Provides live event coverage alongside Film Making Club',
                'description': 'Capturing moments and creating visual stories through photography',
                'highlights': [
                    'Live event coverage',
                    'Photography competitions',
                    'Visual storytelling',
                    'Technical photography skills'
                ],
            },
            {
                'name': 'Film Making Club',
                'short_name': 'FMaC',
                'type': 'club',
                'category': 'Media & Production',
                'role': 'Handles live event coverage in collaboration with Photography Club',
                'description': 'Creating cinematic experiences and documenting festival highlights',
                'highlights': [
                    'Live event filming',
                    'Documentary production',
                    'Video editing workshops',
                    'Cinematic storytelling'
                ],
            },
            
            # Special Clubs
            {
                'name': 'BITS Embryo',
                'short_name': 'Embryo',
                'type': 'club',
                'category': 'Guest Relations & Protocol',
                'role': 'Invites and manages Chief Guests for inauguration ceremony and their hospitality',
                'description': 'Elite club managing VIP relations and protocol for distinguished guests',
                'highlights': [
                    'Chief Guest invitation and coordination',
                    'Inauguration ceremony management',
                    'VIP hospitality services',
                    'Protocol management'
                ],
            },
            {
                'name': 'Mathematics Association',
                'short_name': 'MathAssoc',
                'type': 'club',
                'category': 'Academic & Technical',
                'role': 'Organizes mathematics-related competitions and events',
                'description': 'Promoting mathematical excellence and problem-solving skills',
                'highlights': [
                    'Mathematical competitions',
                    'Problem-solving events',
                    'Academic workshops',
                    'Quantitative skill development'
                ],
            },
            {
                'name': 'Oasis Legacy Team',
                'short_name': 'Legacy',
                'type': 'club',
                'category': 'Heritage & Documentation',
                'role': 'Manages continuity and documentation of festival traditions',
                'description': 'Preserving OASIS heritage and ensuring tradition continuity',
                'highlights': [
                    'Festival tradition documentation',
                    'Heritage preservation',
                    'Continuity management',
                    'Historical archiving'
                ],
            },
            {
                'name': 'Fashion Club',
                'short_name': 'Fashion',
                'type': 'club',
                'category': 'Fashion & Lifestyle',
                'role': 'Organizes fashion shows and style-related events',
                'description': 'Showcasing style, fashion trends, and lifestyle events',
                'highlights': [
                    'Fashion show organization',
                    'Style competitions',
                    'Lifestyle events',
                    'Fashion trend showcases'
                ],
            },
            {
                'name': 'Gurukul',
                'short_name': 'Gurukul',
                'type': 'club',
                'category': 'Cultural Heritage',
                'role': 'Conducts traditional and cultural knowledge-based activities',
                'description': 'Preserving and promoting traditional Indian culture and knowledge',
                'highlights': [
                    'Traditional knowledge events',
                    'Cultural competitions',
                    'Heritage workshops',
                    'Ancient wisdom promotion'
                ],
            },
        ]
        
        # Combine all data
        all_data = major_departments + minor_departments + clubs
        
        created_count = 0
        for item_data in all_data:
            item, created = DepartmentClub.objects.get_or_create(
                name=item_data['name'],
                type=item_data['type'],
                defaults=item_data
            )
            if created:
                created_count += 1
                self.stdout.write(f'Created {item.get_type_display()}: {item.name} ({item.category})')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {created_count} OASIS departments and clubs! '
                f'Total items in database: {DepartmentClub.objects.count()}'
            )
        )
        
        # Summary by category
        self.stdout.write('\\n' + '='*50)
        self.stdout.write('SUMMARY BY CATEGORY:')
        self.stdout.write('='*50)
        
        categories = DepartmentClub.objects.values_list('category', flat=True).distinct()
        for category in sorted(categories):
            count = DepartmentClub.objects.filter(category=category).count()
            items = DepartmentClub.objects.filter(category=category).values_list('name', flat=True)
            self.stdout.write(f'\\n{category} ({count}):')
            for item in items:
                self.stdout.write(f'  - {item}')