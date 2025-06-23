from django.urls import path
from django.shortcuts import render
from . import views

def attendance_success(request):
    return render(request, 'attendance/success.html')

urlpatterns = [
    path('sign-in/', views.daily_sign_in, name='daily_sign_in'),
    path('api/check-in/', views.check_in, name='check_in'),
    path('api/check-out/', views.check_out, name='check_out'),
    path('success/', attendance_success, name='attendance_success'),

]

