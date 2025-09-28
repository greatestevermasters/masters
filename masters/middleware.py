# your_project/middleware.py
import re
from django.conf import settings
from django.shortcuts import redirect

EXEMPT_PATH_PREFIXES = (
    settings.STATIC_URL,     # /static/
    "/media/",
    "/admin/",
    "/summernote/",
    "/access/",
    "/guest/",
    settings.LOGIN_URL,      # /accounts/login/
    settings.LOGOUT_REDIRECT_URL or "/accounts/logout/",
    "/favicon.ico",
)

class RequireLoginMiddleware:
    """
    If user is not authenticated and not a guest, redirect them to /access/?next=...
    Allows access to STATIC, MEDIA, admin, summernote, access/guest/login/logout.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info
        # Allow if already authenticated or already chosen guest
        if request.user.is_authenticated or request.session.get("is_guest"):
            return self.get_response(request)

        # Allow the exempt paths (so login, static, admin, summernote, access, guest work)
        for prefix in EXEMPT_PATH_PREFIXES:
            if prefix and path.startswith(prefix):
                return self.get_response(request)

        # Prevent redirect loop: allow pages in allowed list
        # Finally redirect to access prompt with next
        return redirect(f"/access/?next={path}")
