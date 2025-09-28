from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.core.mail import send_mail

from .forms import (
    CustomUserCreationForm,
    ForgotPasswordForm,
    OTPVerifyForm,
    ResetPasswordForm,
)
from .models import PasswordResetOTP
from content.models import Content   # ✅ unified content model

import random


# ---------------------------
# Signup
# ---------------------------
class SignupView(CreateView):
    """
    User registration view.
    After successful registration user will be logged in automatically
    and redirected to 'home'.
    """
    template_name = "signup.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.request.session.pop("guest", None)
        messages.success(self.request, "Account created and logged in.")
        return redirect("home")


# ---------------------------
# Home / Access / Guest logic
# ---------------------------
def home(request):
    if not request.user.is_authenticated and not request.session.get("guest"):
        return redirect("access_prompt")
    return render(request, "home.html")


def access_prompt(request):
    if request.user.is_authenticated:
        return redirect("home")
    return render(request, "access_prompt.html")


def continue_as_guest(request):
    request.session["guest"] = True
    return redirect("home")


def exit_guest(request):
    request.session.pop("guest", None)
    return redirect("access_prompt")


class CustomLoginView(LoginView):
    template_name = "login.html"

    def form_valid(self, form):
        login(self.request, form.get_user())
        self.request.session.pop("guest", None)
        return redirect("home")


def logout_view(request):
    logout(request)
    request.session.pop("guest", None)
    return redirect("access_prompt")


# ---------------------------
# Search across all masters & types
# ---------------------------
def search(request):
    query = request.GET.get("q", "").strip()
    results = {}

    if query:
        masters = ["buddha", "osho", "krishna"]
        content_types = ["teaching", "book", "video", "blog"]

        for master in masters:
            master_results = {}
            for ctype in content_types:
                qs = Content.objects.filter(
                    master=master,
                    content_type=ctype
                ).filter(
                    Q(title__icontains=query)
                    | Q(description__icontains=query)
                    | Q(excerpt__icontains=query)
                )
                master_results[f"{ctype}s"] = qs  # e.g. 'teachings', 'books'
            results[master] = master_results

    return render(
        request,
        "search_results.html",
        {"query": query, "results": results},
    )


# ---------------------------
# Forgot-Password (Email OTP)
# ---------------------------
def forgot_password_request(request):
    if request.method == "POST":
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            user = get_object_or_404(User, email=email)
            otp = str(random.randint(100000, 999999))
            obj = PasswordResetOTP.objects.create(user=user, otp=otp)

            send_mail(
                subject="Your Password Reset OTP",
                message=f"Your OTP is {otp}. It will expire in 10 minutes.",
                from_email="bltataenglishguru@gmail.com",
                recipient_list=[email],
            )

            request.session["reset_token"] = str(obj.token)
            return redirect("forgot_password_verify")
    else:
        form = ForgotPasswordForm()
    return render(request, "forgot_password.html", {"form": form})


def forgot_password_verify(request):
    token = request.session.get("reset_token")
    obj = get_object_or_404(PasswordResetOTP, token=token)

    if request.method == "POST":
        form = OTPVerifyForm(request.POST)
        if form.is_valid():
            if obj.is_expired():
                messages.error(request, "OTP expired.")
            elif obj.otp == form.cleaned_data["otp"]:
                request.session["verified_user"] = obj.user.id
                return redirect("forgot_password_reset")
            else:
                messages.error(request, "Invalid OTP.")
    else:
        form = OTPVerifyForm()
    return render(request, "forgot_password_verify.html", {"form": form})


def forgot_password_reset(request):
    user_id = request.session.get("verified_user")
    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data["new_password"])
            user.save()
            messages.success(request, "Password changed successfully. You can log in now.")
            return redirect("login")
    else:
        form = ResetPasswordForm()
    return render(request, "forgot_password_reset.html", {"form": form})

