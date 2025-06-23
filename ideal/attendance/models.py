from django.db import models
from django.conf import settings

class AttendanceRecord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    status_choices = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
    ]
    status = models.CharField(max_length=10, choices=status_choices, default='present')
    notes = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('user', 'date') # one record per user per day

    def __str__(self):
        # Use 'username' if it exists, otherwise fallback to string representation of user
        user_display = getattr(self.user, "username", str(self.user))
        return f"{user_display} - {self.date} - {self.status}"



