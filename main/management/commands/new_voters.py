import random
import string
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from main.models import Voter, GensecCandidate, PrezCandidate
import time

# Add the chemical elements here. Replace this list with real data later.
VOTER_NAMES = [
    "Sonia",
    "Rajesh",
    "Anika",
    "Suresh",
    "Asha",
    "Deepak",
    "Rekha",
    "Manish",
    "Shivani",
    "Prakash",
    "Jaya",
    "Alok",
    "Rashmi",
    "Vinod",
    "Sunita",
    "Gaurav",
    "Preeti",
    "Sachin",
    "Neeta",
    "Ramesh",
    "Geeta",
    "Vishal",
    "Radha",
    "Mohan",
    "Shalini" "Aarav Patel",
    "Priya Sharma",
    "Arjun Singh",
    "Neha Gupta",
    "Vikram Malhotra",
    "Anjali Desai",
    "Rahul Choudhury",
    "Meera Reddy",
    "Rohan Kapoor",
    "Kavita Joshi",
]
SLEEP_TIME_INTERVAL = 120
# candidates = {
#     "Zahan Zansal": 3,
#     "Zrish Zain": 4,
#     "Zarvit Zrishnia": 5,
#     "Zaryan Zhorana": 1,
#     "Zadit Zittal": 2
# }
# more names
# "Karthik", "Meera", "Aditya", "Pooja", "Nikhil",
# "Anjali", "Ravi", "Kavya", "Sanjay", "Lakshmi",
# "Akash", "Nisha", "Vijay", "Shreya", "Amit"
# unused
# "Sonia", "Rajesh", "Anika", "Suresh", "Asha",
# "Deepak", "Rekha", "Manish", "Shivani", "Prakash",
# "Jaya", "Alok", "Rashmi", "Vinod", "Sunita",
# "Gaurav", "Preeti", "Sachin", "Neeta", "Ramesh",
# "Geeta", "Vishal", "Radha", "Mohan", "Shalini"
    # "Aarav Patel",
    # "Priya Sharma",
    # "Arjun Singh",
    # "Neha Gupta",
    # "Vikram Malhotra",
    # "Anjali Desai",
    # "Rahul Choudhury",
    # "Meera Reddy",
    # "Rohan Kapoor",
    #----
    # "Kavita Joshi",
    # "Sanjay Mehta",
    # "Divya Saxena",
    # "Aditya Verma",
    # "Nisha Kumar",
    # "Rajesh Bhatia",
    # "Pooja Agarwal",
    # "Amit Khanna",
    # "Sunita Rao",
    # "Vijay Krishnan",
    # "Ananya Mukherjee"


class Command(BaseCommand):
    help = "Populate database with voters and vote for specific candidates."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prez3_votes = 0
        self.prez5_votes = 0
        self.gensec1_votes = 0
        self.gensec2_votes = 0

    def handle(self, *args, **kwargs):
        for voter_name in VOTER_NAMES:
            if User.objects.filter(username__startswith=voter_name).exists():
                self.stdout.write(
                    self.style.WARNING(
                        f"User with name {voter_name} already exists. Skipping."
                    )
                )
                continue

            # Generate a random 3-digit number for the email
            random_number = "".join(random.choices(string.digits, k=3))
            username = f"{voter_name}{random_number}"
            email = f"{username.lower()}@gmail.com"

            # Create a new user with the generated name and email
            user = User.objects.create(username=username, email=email)

            # Create a Voter object for the new user
            voter = Voter.objects.create(user=user, name=voter_name)

            # Randomly choose between general secretary candidates 1 and 2
            gensec_candidate_id = random.choice([1, 2])
            
            # Check vote limits for Gensec candidate 1 (Zaryan) and adjust if necessary
            if gensec_candidate_id == 1 and self.gensec1_votes >= 10:
                gensec_candidate_id = 2

            gensec_candidate = GensecCandidate.objects.get(candidate_id=gensec_candidate_id)

            # Update Gensec vote counts
            if gensec_candidate_id == 1:
                self.gensec1_votes += 1
            else:
                self.gensec2_votes += 1

            # Randomly choose between presidential candidates 3 and 5
            prez_candidate_id = random.choice([3, 5])
            
            # Check vote limits and adjust if necessary
            if prez_candidate_id == 3 and self.prez3_votes >= 20:
                prez_candidate_id = 5
            elif prez_candidate_id == 5 and self.prez5_votes >= 25:
                prez_candidate_id = 3

            prez_candidate = PrezCandidate.objects.get(candidate_id=prez_candidate_id)

            # Update Prez vote counts
            if prez_candidate_id == 3:
                self.prez3_votes += 1
            else:
                self.prez5_votes += 1

            # Vote for the candidates
            voter.gensec = gensec_candidate
            voter.prez = prez_candidate
            voter.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f"Voter {voter.name} created and voted for Gensec {gensec_candidate.name} and Prez {prez_candidate.name}."
                )
            )

            # Wait for the specified interval before the next iteration
            time.sleep(SLEEP_TIME_INTERVAL)

        self.stdout.write(
            self.style.SUCCESS("All elements have been processed. Stopping job.")
        )
        self.stdout.write(
            self.style.SUCCESS(f"Final vote count - Gensec 1 (Zaryan): {self.gensec1_votes}, Gensec 2: {self.gensec2_votes}, Prez 3: {self.prez3_votes}, Prez 5: {self.prez5_votes}")
        )


# script rules
# docker exec -it pollz_web python manage.py populate_voters
# To keep this running even if you close your terminal session, you can use nohup or run it in a screen session:
# docker exec -it pollz_web nohup python manage.py populate_voters > populate_voters.log 2>&1 &

# If you need to stop the script before it completes, you can find its process ID and kill it:

# docker exec -it pollz_web ps aux | grep populate_voters
# docker exec -it pollz_web kill <PID>
# Replace <PID> with the process ID you find from the first command.

# This script now:

# Takes names sequentially from the VOTER_NAMES list.
# Checks if a user with that name already exists before creating a new one.
# Creates a new user and voter for each name in the list.
# Randomly chooses between general secretary candidates 1 and 2, with a max of 10 votes for candidate 1 (Zaryan).
# Randomly chooses between presidential candidates 3 and 5, with vote limits.
# Waits for the specified SLEEP_TIME_INTERVAL between each iteration.
# Stops automatically after processing all names in the list.
# Keeps all comments and unused code as requested.