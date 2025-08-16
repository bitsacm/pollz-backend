from django.core.management.base import BaseCommand
from main.models import Department, Huel

class Command(BaseCommand):
    help = 'Populate database with complete HUEL courses data (40 courses)'

    def handle(self, *args, **options):
        self.stdout.write('Creating complete HUEL courses data...')
        
        # Create HSS and GS departments if they don't exist
        hss_dept, _ = Department.objects.get_or_create(
            short_name='HSS',
            defaults={'name': 'Humanities and Social Sciences'}
        )
        
        gs_dept, _ = Department.objects.get_or_create(
            short_name='GS',
            defaults={'name': 'General Studies'}
        )
        
        bits_dept, _ = Department.objects.get_or_create(
            short_name='BITS',
            defaults={'name': 'BITS Pilani Institute'}
        )
        
        # Complete list of 40 HUEL courses
        huels_data = [
            # HSS Courses
            {
                'code': 'HSS F236',
                'name': 'Symbolic Logic',
                'department': hss_dept,
                'instructor': 'Dr. Philosophy',
                'description': 'Introduction to formal logic and symbolic reasoning',
            },
            {
                'code': 'HSS F334',
                'name': 'Srimad Bhagavad Gita',
                'department': hss_dept,
                'instructor': 'Prof. Vedanta',
                'description': 'Study of ancient Indian philosophical text',
            },
            {
                'code': 'HSS F328',
                'name': 'Human Resource Development',
                'department': hss_dept,
                'instructor': 'Dr. Management',
                'description': 'Principles and practices of human resource management',
            },
            {
                'code': 'HSS 224',
                'name': 'English Skills for Academics',
                'department': hss_dept,
                'instructor': 'Prof. English',
                'description': 'Academic writing and communication skills',
            },
            {
                'code': 'HSS F227',
                'name': 'Cross Cultural Skills',
                'department': hss_dept,
                'instructor': 'Dr. Culture',
                'description': 'Understanding diverse cultures and communication',
            },
            {
                'code': 'HSS F346',
                'name': 'International Relations',
                'department': hss_dept,
                'instructor': 'Prof. Politics',
                'description': 'Global politics and international affairs',
            },
            {
                'code': 'HSS F325',
                'name': 'Cinematic Adaptation',
                'department': hss_dept,
                'instructor': 'Dr. Cinema',
                'description': 'Literature to film adaptations and analysis',
            },
            {
                'code': 'HSS F343',
                'name': 'Professional Ethics',
                'department': hss_dept,
                'instructor': 'Prof. Ethics',
                'description': 'Ethical principles in professional practice',
            },
            {
                'code': 'HSS F223',
                'name': 'Appreciation of Indian Music',
                'department': hss_dept,
                'instructor': 'Dr. Music',
                'description': 'Classical and contemporary Indian music forms',
            },
            {
                'code': 'HSS F323',
                'name': 'Organizational Psychology',
                'department': hss_dept,
                'instructor': 'Dr. Psychology',
                'description': 'Psychological principles in workplace settings',
            },
            {
                'code': 'HSS F222',
                'name': 'Linguistics',
                'department': hss_dept,
                'instructor': 'Prof. Language',
                'description': 'Scientific study of language and communication',
            },
            {
                'code': 'HSS F368',
                'name': 'Asian Cinemas and Cultures',
                'department': hss_dept,
                'instructor': 'Dr. Asian Studies',
                'description': 'Exploration of Asian film and cultural traditions',
            },
            {
                'code': 'HSS F235',
                'name': 'Introductory Philosophy',
                'department': hss_dept,
                'instructor': 'Prof. Philosophy',
                'description': 'Basic concepts and problems in philosophy',
            },
            {
                'code': 'HSS F234',
                'name': 'Main Currents of Modern History',
                'department': hss_dept,
                'instructor': 'Dr. History',
                'description': 'Major historical developments in modern era',
            },
            {
                'code': 'HSS F221',
                'name': 'Readings from Drama',
                'department': hss_dept,
                'instructor': 'Prof. Literature',
                'description': 'Analysis of dramatic works and theatre',
            },
            {
                'code': 'HSS F345',
                'name': 'Gandhian Thoughts',
                'department': hss_dept,
                'instructor': 'Dr. Gandhi Studies',
                'description': 'Philosophy and principles of Mahatma Gandhi',
            },
            {
                'code': 'HSS F332',
                'name': 'Cinematic Art',
                'department': hss_dept,
                'instructor': 'Prof. Film Studies',
                'description': 'Artistic and technical aspects of cinema',
            },
            
            # GS Courses
            {
                'code': 'GS 243',
                'name': 'Current Affairs',
                'department': gs_dept,
                'instructor': 'Prof. Current Events',
                'description': 'Contemporary national and international issues',
            },
            {
                'code': 'GS F224',
                'name': 'Print and Audio-Visual Advertising',
                'department': gs_dept,
                'instructor': 'Dr. Advertising',
                'description': 'Creative and strategic aspects of advertising',
            },
            {
                'code': 'GS F223',
                'name': 'Introduction to Mass Communication',
                'department': gs_dept,
                'instructor': 'Prof. Media',
                'description': 'Fundamentals of mass media and communication',
            },
            {
                'code': 'GS F332',
                'name': 'Contemporary India',
                'department': gs_dept,
                'instructor': 'Dr. Indian Studies',
                'description': 'Modern India: society, politics, and economy',
            },
            {
                'code': 'GS F212',
                'name': 'Environment, Development and Climate Change',
                'department': gs_dept,
                'instructor': 'Prof. Environment',
                'description': 'Environmental issues and sustainable development',
            },
            {
                'code': 'GS F334',
                'name': 'Copywriting',
                'department': gs_dept,
                'instructor': 'Dr. Creative Writing',
                'description': 'Professional writing for advertising and marketing',
            },
            {
                'code': 'GS 247',
                'name': 'Social Informatics',
                'department': gs_dept,
                'instructor': 'Prof. Social Computing',
                'description': 'Impact of information technology on society',
            },
            {
                'code': 'GS F244',
                'name': 'Report and Writing for Media',
                'department': gs_dept,
                'instructor': 'Dr. Journalism',
                'description': 'News writing and media reporting techniques',
            },
            {
                'code': 'GS F245',
                'name': 'Effective Public Speaking',
                'department': gs_dept,
                'instructor': 'Prof. Communication',
                'description': 'Public speaking and presentation skills',
            },
            {
                'code': 'GS F334',
                'name': 'Global Business and Tech',
                'department': gs_dept,
                'instructor': 'Dr. Global Business',
                'description': 'Technology\'s role in international business',
            },
            {
                'code': 'GS F222',
                'name': 'Language Lab Practice',
                'department': gs_dept,
                'instructor': 'Prof. Language',
                'description': 'Practical language learning exercises',
            },
            {
                'code': 'GS F312',
                'name': 'Applied Philosophy',
                'department': gs_dept,
                'instructor': 'Dr. Applied Ethics',
                'description': 'Practical applications of philosophical thinking',
            },
            {
                'code': 'GS F333',
                'name': 'Public Administration',
                'department': gs_dept,
                'instructor': 'Prof. Administration',
                'description': 'Principles of public sector management',
            },
            {
                'code': 'GS F321',
                'name': 'Mass Media and Content Design',
                'department': gs_dept,
                'instructor': 'Dr. Media Design',
                'description': 'Content creation for various media platforms',
            },
            {
                'code': 'GS F221',
                'name': 'Business Communication',
                'department': gs_dept,
                'instructor': 'Prof. Business',
                'description': 'Professional communication in business context',
            },
            {
                'code': 'GS F211',
                'name': 'Modern Political Concepts',
                'department': gs_dept,
                'instructor': 'Dr. Political Science',
                'description': 'Contemporary political theories and concepts',
            },
            {
                'code': 'GS F331',
                'name': 'Techniques in Social Research',
                'department': gs_dept,
                'instructor': 'Prof. Research Methods',
                'description': 'Methodology for social science research',
            },
            {
                'code': 'GS F232',
                'name': 'Introductory Psychology',
                'department': gs_dept,
                'instructor': 'Dr. Psychology',
                'description': 'Basic principles of human psychology',
            },
            {
                'code': 'GS F322',
                'name': 'Critical Analysis of Literature and Cinema',
                'department': gs_dept,
                'instructor': 'Prof. Critical Studies',
                'description': 'Analytical approaches to literature and film',
            },
            {
                'code': 'GS F311',
                'name': 'Introduction to Conflict Management',
                'department': gs_dept,
                'instructor': 'Dr. Conflict Resolution',
                'description': 'Strategies for resolving conflicts and disputes',
            },
            {
                'code': 'GS F343',
                'name': 'Short Film Production',
                'department': gs_dept,
                'instructor': 'Prof. Film Production',
                'description': 'Practical aspects of short film making',
            },
            {
                'code': 'GS F231',
                'name': 'Dynamics of Social Change',
                'department': gs_dept,
                'instructor': 'Dr. Sociology',
                'description': 'Understanding social transformation processes',
            },
            
            # BITS Course
            {
                'code': 'BITS F226',
                'name': 'Soft Skills for Professionals',
                'department': bits_dept,
                'instructor': 'Prof. Professional Development',
                'description': 'Essential soft skills for professional success',
            },
        ]
        
        created_count = 0
        for huel_data in huels_data:
            huel, created = Huel.objects.get_or_create(
                code=huel_data['code'],
                defaults=huel_data
            )
            if created:
                created_count += 1
                self.stdout.write(f'Created HUEL: {huel.code} - {huel.name}')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {created_count} new HUEL courses! '
                f'Total HUELs in database: {Huel.objects.count()}'
            )
        )