from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
import re

letters_only = RegexValidator(r"^[A-Za-z ]+$", "Only letters and spaces are allowed.")
digits_only  = RegexValidator(r"^[0-9]+$", "Only numbers are allowed.")

class RegisterForm(forms.Form):
    name = forms.CharField(
        max_length=80,
        validators=[letters_only],
        widget=forms.TextInput(attrs={"class":"form-control form-pill reveal-up"})
    )
    mobile = forms.CharField(
        max_length=15,
        validators=[digits_only],
        widget=forms.TextInput(attrs={"class":"form-control form-pill reveal-up"})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class":"form-control form-pill reveal-up"})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class":"form-control form-pill reveal-up"})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class":"form-control form-pill reveal-up"})
    )

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("User already exists — try to login.")
        return email

    def _validate_password_strength(self, pwd: str):
        """
        Returns a list of error messages for password strength violations.
        Rules: 8+ chars, 1 uppercase, 1 lowercase, 1 digit, 1 special.
        """
        errors = []
        if len(pwd) < 8:
            errors.append("Password must be at least 8 characters.")
        if not re.search(r"[A-Z]", pwd):
            errors.append("Include at least one uppercase letter (A–Z).")
        if not re.search(r"[a-z]", pwd):
            errors.append("Include at least one lowercase letter (a–z).")
        if not re.search(r"\d",  pwd):
            errors.append("Include at least one number (0–9).")
        if not re.search(r"[!@#$%^&*()_\-+=\[{\]};:'\",.<>/?\\|`~]", pwd):
            errors.append("Include at least one special character (e.g., ! @ #).")
        return errors
    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1") or ""
        p2 = cleaned.get("password2") or ""

        # Match check
        if p1 and p2 and p1 != p2:
            self.add_error("password2", "Passwords do not match.")

        # Strength check with clear messages
        if p1:
            for msg in self._validate_password_strength(p1):
                self.add_error("password1", msg)

        return cleaned


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class":"form-control form-pill reveal-up"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class":"form-control form-pill reveal-up"})
    )

# partner page
from django import forms
from django.core.validators import RegexValidator
from .models import PartnerApplication, PartnerCity

letters_only = RegexValidator(r"^[A-Za-z ]+$", "Only letters and spaces are allowed.")
digits_only  = RegexValidator(r"^[0-9]+$", "Only numbers are allowed.")

class PartnerApplyForm(forms.ModelForm):
    name = forms.CharField(
        max_length=80, validators=[letters_only],
        widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"Your Name"})
    )
    phone = forms.CharField(
        max_length=15, validators=[digits_only],
        widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"Phone Number"})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class":"form-control", "placeholder":"E-Mail Id"})
    )
    city = forms.ModelChoiceField(
        queryset=PartnerCity.objects.none(),
        widget=forms.Select(attrs={"class":"form-select form-control-like", "placeholder":"Select a City"})
    )
    pincode = forms.CharField(
        max_length=10, validators=[digits_only],
        widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"Pin Code"})
    )

    class Meta:
        model = PartnerApplication
        fields = ("name", "phone", "email", "city", "pincode")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["city"].queryset = PartnerCity.objects.all()

    def clean_phone(self):
        ph = self.cleaned_data["phone"]
        if len(ph) < 10:
            raise forms.ValidationError("Enter a valid 10-digit phone number.")
        return ph

    def clean_pincode(self):
        pin = self.cleaned_data["pincode"]
        if len(pin) < 6:
            raise forms.ValidationError("Enter a valid 6-digit PIN code.")
        return pin
