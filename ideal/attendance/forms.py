from django import forms
from .models import AttendanceRecord

class DailySignInForm(forms.ModelForm):
    class Meta:
        model = AttendanceRecord
        fields = ['check_in_time', 'status', 'notes']
        widgets = {
            'check_in_time': forms.TimeInput(attrs={'type': 'time'}),
            'status': forms.Select(),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
