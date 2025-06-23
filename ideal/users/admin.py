from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'user_type', 'is_staff', 'is_active')
    list_filter = ('user_type', 'is_staff', 'is_active')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Only allow staff users to be visible in admin
        if request.user.is_superuser:
            return qs
        return qs.filter(user_type='staff')

    def has_module_permission(self, request):
        return request.user.is_authenticated and request.user.is_staff_member()

admin.site.register(CustomUser, CustomUserAdmin)
