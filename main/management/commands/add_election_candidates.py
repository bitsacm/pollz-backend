from django.core.management.base import BaseCommand
from main.models import ElectionPosition, ElectionCandidate

class Command(BaseCommand):
    help = 'Add election candidates for President and General Secretary positions'

    def handle(self, *args, **options):
        # Create or get positions
        president_position, _ = ElectionPosition.objects.get_or_create(
            name="President",
            defaults={'description': 'Student Union President', 'is_active': True}
        )
        
        gensec_position, _ = ElectionPosition.objects.get_or_create(
            name="General Secretary",
            defaults={'description': 'Student Union General Secretary', 'is_active': True}
        )
        
        # President candidates
        president_candidates = [
            {
                'name': 'Sajal Yadav',
                'party': 'Progressive Alliance',
                'manifesto': 'Committed to enhancing student welfare through improved facilities, transparent governance, and inclusive policies for all.',
                'agenda': [
                    'Improve campus infrastructure',
                    'Enhance placement opportunities',
                    'Transparent student governance',
                    'Mental health support programs'
                ],
                'image': 'https://ui-avatars.com/api/?name=Sajal+Yadav&background=FFC107&color=000'
            },
            {
                'name': 'Tarang Agarwal',
                'party': 'Student First',
                'manifesto': 'Focus on academic excellence, research opportunities, and creating a vibrant campus culture that nurtures innovation.',
                'agenda': [
                    'Research funding for students',
                    'Industry collaboration programs',
                    'Cultural fest expansion',
                    'Skill development workshops'
                ],
                'image': 'https://ui-avatars.com/api/?name=Tarang+Agarwal&background=FFC107&color=000'
            },
            {
                'name': 'Daksh Tyagi',
                'party': 'Unity Front',
                'manifesto': 'Building bridges between administration and students, ensuring every voice is heard and every concern addressed.',
                'agenda': [
                    'Regular town halls with admin',
                    'Student grievance portal',
                    'Campus safety initiatives',
                    'Green campus projects'
                ],
                'image': 'https://ui-avatars.com/api/?name=Daksh+Tyagi&background=FFC107&color=000'
            },
            {
                'name': 'Shrinath Bhimrao Golhar',
                'party': 'Independent',
                'manifesto': 'Independent voice for student rights, focusing on transparency, accountability, and sustainable campus development.',
                'agenda': [
                    'Hostel renovation projects',
                    'Food quality improvement',
                    'Sports facility upgrades',
                    'Entrepreneurship support'
                ],
                'image': 'https://ui-avatars.com/api/?name=Shrinath+Golhar&background=FFC107&color=000'
            }
        ]
        
        # General Secretary candidates
        gensec_candidates = [
            {
                'name': 'Anuj Wagh',
                'party': 'Progressive Alliance',
                'manifesto': 'Dedicated to streamlining administrative processes and ensuring efficient communication between students and management.',
                'agenda': [
                    'Digital documentation system',
                    'Quick grievance resolution',
                    'Student portal enhancement',
                    'Academic calendar optimization'
                ],
                'image': 'https://ui-avatars.com/api/?name=Anuj+Wagh&background=FFC107&color=000'
            },
            {
                'name': 'Priyadarshi Rishabh',
                'party': 'Student First',
                'manifesto': 'Committed to academic reforms, examination transparency, and creating better learning environments for all.',
                'agenda': [
                    'Exam pattern reforms',
                    'Library modernization',
                    'Study space expansion',
                    'Peer learning programs'
                ],
                'image': 'https://ui-avatars.com/api/?name=Priyadarshi+Rishabh&background=FFC107&color=000'
            },
            {
                'name': 'Apoorv Singh',
                'party': 'Unity Front',
                'manifesto': 'Focus on student welfare, health services improvement, and creating inclusive policies for diverse student needs.',
                'agenda': [
                    'Health center upgrades',
                    'Counseling services expansion',
                    'Inclusive policy framework',
                    'Emergency support systems'
                ],
                'image': 'https://ui-avatars.com/api/?name=Apoorv+Singh&background=FFC107&color=000'
            }
        ]
        
        # Add President candidates
        self.stdout.write('Adding President candidates...')
        for candidate_data in president_candidates:
            candidate, created = ElectionCandidate.objects.update_or_create(
                name=candidate_data['name'],
                position=president_position,
                defaults={
                    'party': candidate_data['party'],
                    'manifesto': candidate_data['manifesto'],
                    'agenda': candidate_data['agenda'],
                    'image': candidate_data['image'],
                    'is_active': True,
                    'vote_count': 0
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created President candidate: {candidate.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Updated President candidate: {candidate.name}'))
        
        # Add General Secretary candidates
        self.stdout.write('Adding General Secretary candidates...')
        for candidate_data in gensec_candidates:
            candidate, created = ElectionCandidate.objects.update_or_create(
                name=candidate_data['name'],
                position=gensec_position,
                defaults={
                    'party': candidate_data['party'],
                    'manifesto': candidate_data['manifesto'],
                    'agenda': candidate_data['agenda'],
                    'image': candidate_data['image'],
                    'is_active': True,
                    'vote_count': 0
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created GenSec candidate: {candidate.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Updated GenSec candidate: {candidate.name}'))
        
        # Display summary
        total_president = ElectionCandidate.objects.filter(position=president_position, is_active=True).count()
        total_gensec = ElectionCandidate.objects.filter(position=gensec_position, is_active=True).count()
        
        self.stdout.write(self.style.SUCCESS(f'\nSummary:'))
        self.stdout.write(self.style.SUCCESS(f'Total President candidates: {total_president}'))
        self.stdout.write(self.style.SUCCESS(f'Total General Secretary candidates: {total_gensec}'))
        self.stdout.write(self.style.SUCCESS('Election candidates added successfully!'))