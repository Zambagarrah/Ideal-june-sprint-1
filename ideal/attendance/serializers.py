from rest_framework import serializers
from .models import AttendanceRecord

class AttendanceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceRecord
        fields = ['id', 'user', 'date', 'check_in_time', 'check_out_time', 'status', 'notes']
        read_only_fields = ['user', 'date']
