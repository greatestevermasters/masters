# masters/decorators.py
from functools import wraps
from django.shortcuts import redirect
from django.conf import settings
from django.contrib import messages

def require_full_auth(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        messages.error(request, "Please login to perform that action.")
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")
    return _wrapped
