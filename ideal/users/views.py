from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import redirect

def staff_required(view_func):
    decorated_view_func = login_required(
        user_passes_test(lambda u: u.is_authenticated and u.user_type == 'staff')(view_func)
    )
    return decorated_view_func

def community_required(view_func):
    decorated_view_func = login_required(
        user_passes_test(lambda u: u.is_authenticated and u.user_type == 'community')(view_func)
    )
    return decorated_view_func
