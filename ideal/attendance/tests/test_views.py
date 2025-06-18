from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from attendance.models import AttendanceRecord
from attendance.forms import DailySignInForm
from datetime import date
from django.utils.timezone import now

User = get_user_model()

class DailySignInViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='viewuser', email='view@example.com', password='password', user_type='community')
        self.login_url = reverse('daily_sign_in') # Assuming you named your URL pattern 'daily_sign_in'

    def test_daily_sign_in_view_redirects_if_not_logged_in(self):
        response = self.client.get(self.login_url)
        # Check that it redirects to login page if user is not authenticated
        self.assertRedirects(response, f'/accounts/login/?next={self.login_url}')

    def test_daily_sign_in_view_get(self):
        self.client.login(username='viewuser', password='password')
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'attendance/daily_sign_in.html')
        self.assertIsInstance(response.context['form'], DailySignInForm)

    def test_daily_sign_in_view_post_success(self):
        self.client.login(username='viewuser', password='password')
        data = {
            'check_in_time': now().strftime('%H:%M'), # Format to HH:MM
            'status': 'present',
            'notes': 'Test notes',
        }
        response = self.client.post(self.login_url, data)
        self.assertTrue(AttendanceRecord.objects.filter(user=self.user, date=date.today()).exists())
        self.assertRedirects(response, reverse('attendance_success')) # Assuming 'attendance_success' is your redirect URL
