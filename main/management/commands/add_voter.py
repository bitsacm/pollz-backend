from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from main.models import Voter, GensecCandidate, PrezCandidate

class Command(BaseCommand):
    help = "Add a voter to the database"

    def add_arguments(self, parser):
        parser.add('email', type=str, help='Email of the user')
        parser.add('--gensec', type=str, help='Name of the Gensec candidate', required=False)
        parser.add('--prez', type=str, help='Name of the Prez candidate', required=False)

    def handle(self, *args, **kwargs):
        email = kwargs['email']
        gensec_name = kwargs.get('gensec', None)
        prez_name = kwargs.get('prez', None)

        if gensec_name is None and prez_name is None:
            self.stdout.write(self.style.ERROR("At least one of --gensec or --prez is required"))
            return

        # Get or create User by Email
        try:
            user = User.objects.get(email=email)
            self.stdout.write(self.style.ERROR(f"User with email {email} already exists"))

        except User.DoesNotExist:
            user = User.objects.create_user(email, email, email)
            user.save()
        
        # Get the Gensec and Prez candidates (if provided)
        gensec_candidate = None
        perz_canadidate = None

        if gensec_name:
            try:
                gensec_candidate = GensecCandidate.objects.get(name__icontains=gensec_name)
            except GensecCandidate.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Gensec candidate with name {gensec_name} does not exist"))
                return

        if prez_name:
            try:
                prez_candidate = PrezCandidate.objects.get(name__icontains=prez_name)
            except:
                self.stdout.write(self.style.ERROR(f"Prez candidate with name {prez_name} does not exist"))
                return

        # Create the Voter
        voter, created = Voter.objects.get_or_create(
                user=user,
                defaults={
                    'name':user.get_full_name(),
                    'gensec':gensec_candidate,
                    'prez':prez_candidate
                }
            )

        if created:
            self.stdout.write(self.style.SUCCESS(f"Voter {voter.name} created successfully"))
        else:
            self.stdout.write(self.style.WARNING(f"Voter {voter.name} already exists"))
            
