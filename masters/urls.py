from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views  # masters/views.py
from .views import healthz


urlpatterns = [
    path("admin/", admin.site.urls),

    path("healthz/", healthz),   # ✅ Health check endpoint
    # Your apps
    path("content/", include("content.urls")),
    path("social/", include("social.urls")),
        # Third-party apps
    path("summernote/", include("django_summernote.urls")),


    # Authentication & signup
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path('forgot-password/', views.forgot_password_request, name='forgot_password'),
    path('forgot-password/verify/', views.forgot_password_verify, name='forgot_password_verify'),
    path('forgot-password/reset/', views.forgot_password_reset, name='forgot_password_reset'),

    # Guest / Access Flow
    path("", views.home, name="home"),
    path("access/", views.access_prompt, name="access_prompt"),
    path("guest/continue/", views.continue_as_guest, name="guest"),
    path("guest/exit/", views.exit_guest, name="exit_guest"),

    # Search
    path("search/", views.search, name="search"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
