from django.test import TestCase
from django.contrib.auth import get_user_model
from attendance.models import AttendanceRecord
from datetime import date
from django.db.utils import IntegrityError

User = get_user_model()

class AttendanceRecordModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password', user_type='community')

    def test_create_attendance_record(self):
        record = AttendanceRecord.objects.create(user=self.user, date=date.today(), status='present')
        self.assertEqual(record.user, self.user)
        self.assertEqual(record.date, date.today())
        self.assertEqual(record.status, 'present')

    def test_unique_together_constraint(self):
        AttendanceRecord.objects.create(user=self.user, date=date.today(), status='present')
        with self.assertRaises(IntegrityError):
            AttendanceRecord.objects.create(user=self.user, date=date.today(), status='late')
