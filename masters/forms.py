from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=False, help_text="")
    mobile = forms.CharField(max_length=10, required=False, help_text="")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "mobile", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove default help_text provided by Django
        self.fields["password1"].help_text = None
        self.fields["password2"].help_text = None
        self.fields["username"].help_text = None

    def clean_mobile(self):
        mobile = self.cleaned_data.get("mobile", "")
        if mobile:
            # ensure exactly 10 digits
            if not re.fullmatch(r"\d{10}", mobile):
                raise forms.ValidationError("Enter a valid 10-digit mobile number.")
        return mobile

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        mobile = cleaned_data.get("mobile")

        # Require at least one of email or mobile
        if not email and not mobile:
            raise forms.ValidationError(
                "Please provide either an Email address or a 10-digit Mobile number."
            )
        return cleaned_data


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()


class OTPVerifyForm(forms.Form):
    otp = forms.CharField(
        max_length=6,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-yellow-400 focus:border-yellow-400 bg-white/90 text-gray-900 text-center',
            'placeholder': 'Enter OTP',
        })
    )

class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("new_password") != cleaned.get("confirm_password"):
            raise forms.ValidationError("Passwords do not match.")
        return cleaned
    
email = forms.EmailField(
    widget=forms.EmailInput(attrs={
        'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-yellow-400 focus:border-yellow-400 bg-white/90 text-gray-900',
        'placeholder': 'Enter your email'
    })
)
