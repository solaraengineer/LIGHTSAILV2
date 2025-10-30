from django import forms
import re
from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(widget=forms.PasswordInput, required=True, label="Confirm Password")
    referral = forms.CharField(max_length=50, required=False)
    is_company = forms.BooleanField(required=False, label="Firma")

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if len(password) < 6 or not re.search(r"[A-Z]", password):
            raise forms.ValidationError("Password must be at least 6 characters and contain an uppercase letter.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords do not match.")


class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)


class UpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=False)
    email = forms.EmailField(required=False)
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    city = forms.CharField(max_length=150, required=False)
    address = forms.CharField(max_length=150, required=False)
    country = forms.CharField(max_length=150, required=False)
    account_type = forms.ChoiceField(choices=[('User', 'User'), ('Firma', 'Firma')], required=False)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "address",
            "city",
            "country",
            "account_type",
        ]