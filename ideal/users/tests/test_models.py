from django.test import TestCase
from users.models import CustomUser

class CustomUserModelTest(TestCase):
    def test_create_staff_user(self):
        staff_user = CustomUser.objects.create_user(
            username='stafftest', email='staff@example.com', password='password', user_type='staff'
        )
        self.assertTrue(staff_user.is_staff_member())
        self.assertFalse(staff_user.is_community_member())
        self.assertFalse(staff_user.is_staff) # CustomUser's is_staff can be different from Django's

    def test_create_community_user(self):
        community_user = CustomUser.objects.create_user(
            username='communitytest', email='community@example.com', password='password', user_type='community'
        )
        self.assertTrue(community_user.is_community_member())
        self.assertFalse(community_user.is_staff_member())
        self.assertFalse(community_user.is_staff)
