import email
from genericpath import exists
from os import pipe2
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserRegistrationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    password1 = forms.CharField(
        label="Password", widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    password2 = forms.CharField(
        label="confirm Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    def clean(self):
        cd = super().clean()
        p1 = cd.get("password1")
        p2 = cd.get("password2")
        email = cd.get("email")
        username = cd.get("username")
        user = User.objects.filter(username=username).exists()
        email = User.objects.filter(email=email).exists()
        if p1 and p2 and p1 != p2:
            raise ValidationError("Passwords must be Match")
        elif user:
            raise ValidationError(
                "Please Change The Username, This Username Already Exists"
            )
        elif email:
            raise ValidationError("This Email Already Exists")


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
