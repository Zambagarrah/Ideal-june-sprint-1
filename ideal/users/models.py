from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('staff', 'Staff'),
        ('community', 'Community Member'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)

    def is_staff_member(self):
        return self.user_type == 'staff'

    def is_community_member(self):
        return self.user_type == 'community'
