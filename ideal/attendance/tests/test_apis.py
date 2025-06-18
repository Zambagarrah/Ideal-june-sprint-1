from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from attendance.models import AttendanceRecord
from datetime import date
from django.utils.timezone import now

User = get_user_model()

class AttendanceAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='apiuser', email='api@example.com', password='password', user_type='community'
        )
        self.client.force_authenticate(user=self.user)  # Authenticate the client for API requests

    def test_check_in_success(self):
        url = '/attendance/api/check-in/'
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['check_in_time'])
        self.assertEqual(response.data['user'], self.user.id)
        self.assertTrue(AttendanceRecord.objects.filter(user=self.user, date=date.today()).exists())

    def test_check_in_already_checked_in(self):
        # First check-in
        AttendanceRecord.objects.create(user=self.user, date=date.today(), check_in_time=now().time())
        url = '/attendance/api/check-in/'
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Already checked in today.')

    def test_check_out_success(self):
        # Must check in first
        AttendanceRecord.objects.create(user=self.user, date=date.today(), check_in_time=now().time())
        url = '/attendance/api/check-out/'
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['check_out_time'])
        record = AttendanceRecord.objects.get(user=self.user, date=date.today())
        self.assertIsNotNone(record.check_out_time)

    def test_check_out_not_checked_in_first(self):
        url = '/attendance/api/check-out/'
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'You have not checked in today.')

    def test_check_out_already_checked_out(self):
        # Check in and out
        AttendanceRecord.objects.create(
            user=self.user,
            date=date.today(),
            check_in_time=now().time(),
            check_out_time=now().time()
        )
        url = '/attendance/api/check-out/'
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Already checked out today.')

    def test_check_in_unauthenticated(self):
        self.client.force_authenticate(user=None)  # Remove authentication
        url = '/attendance/api/check-in/'
        response = self.client.post(url, format='json')
        # Expect 403 Forbidden due to SessionAuthentication CSRF enforcement
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
