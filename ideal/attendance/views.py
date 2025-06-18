from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils.timezone import now
from .models import AttendanceRecord
from .serializers import AttendanceRecordSerializer
from django.core.exceptions import ValidationError
from .forms import DailySignInForm


@login_required
def daily_sign_in(request):
    if request.method == 'POST':
        form = DailySignInForm(request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.user = request.user
            attendance.save()
            return redirect('attendance_success')  # Redirect after successful sign-in
    else:
        form = DailySignInForm()
    return render(request, 'attendance/daily_sign_in.html', {'form': form})



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def check_in(request):
    user = request.user
    today = now().date()
    attendance, created = AttendanceRecord.objects.get_or_create(user=user, date=today)
    if attendance.check_in_time:
        return Response({"detail": "Already checked in today."}, status=status.HTTP_400_BAD_REQUEST)
    attendance.check_in_time = now().time()
    attendance.status = 'present'
    attendance.save()
    serializer = AttendanceRecordSerializer(attendance)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def check_out(request):
    user = request.user
    today = now().date()
    try:
        attendance = AttendanceRecord.objects.get(user=user, date=today) # type: ignore
    except AttendanceRecord.DoesNotExist: # type: ignore
        return Response({"detail": "You have not checked in today."}, status=status.HTTP_400_BAD_REQUEST)
    if attendance.check_out_time:
        return Response({"detail": "Already checked out today."}, status=status.HTTP_400_BAD_REQUEST)
    attendance.check_out_time = now().time()
    attendance.save()
    serializer = AttendanceRecordSerializer(attendance)
    return Response(serializer.data, status=status.HTTP_200_OK)

