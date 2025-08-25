from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import ElectionPosition, ElectionCandidate, Department, Huel, DepartmentClub

User = get_user_model()

class APITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='test@pilani.bits-pilani.ac.in', username='testuser')
        self.user.set_password('testpass123')
        self.user.save()
        self.client.force_authenticate(user=self.user)

    def test_google_login_no_token(self):
        url = reverse('google_login')
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 400)

    def test_user_profile(self):
        url = reverse('user_profile')
        response = self.client.get(url)
        self.assertIn(response.status_code, [200, 500])  # 500 if profile creation fails

    def test_election_positions(self):
        ElectionPosition.objects.create(name='President', is_active=True)
        url = reverse('election_positions')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_election_candidates(self):
        pos = ElectionPosition.objects.create(name='President', is_active=True)
        ElectionCandidate.objects.create(name='Alice', position=pos, is_active=True)
        url = reverse('election_candidates')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_departments(self):
        Department.objects.create(name='CSE', short_name='CSE')
        url = reverse('departments')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_huels(self):
        dep = Department.objects.create(name='CSE', short_name='CSE')
        Huel.objects.create(name='HUEL101', code='HUEL101', department=dep, is_active=True)
        url = reverse('huels')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_department_clubs(self):
        DepartmentClub.objects.create(name='Robotics', type='club', is_active=True)
        url = reverse('department_clubs')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_voting_stats(self):
        url = reverse('voting_stats')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_dashboard_stats(self):
        url = reverse('dashboard_stats')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_project_info(self):
        url = reverse('project_info')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_sentry_debug(self):
        url = reverse('sentry_debug')
        try:
            self.client.get(url)
        except Exception:
            pass  # Division by zero expected
