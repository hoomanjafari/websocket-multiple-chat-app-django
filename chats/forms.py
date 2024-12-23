from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from .models import (Member, Message, ChatGroup)


class UserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=66)
    email = forms.EmailField()
    password = forms.CharField(max_length=22)
    password_confirm = forms.CharField(max_length=22)

    def clean_password_confirm(self):
        p1 = self.cleaned_data.get('password')
        p2 = self.cleaned_data.get('password_confirm')

        if p1 and p2:
            if p1 != p2:
                raise ValidationError('passwords do not match')
        return p2

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username

        raise ValidationError('Username is already exists')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=66)
    password = forms.CharField(max_length=22)


class CreateGroupForm(forms.Form):
    group_name = forms.CharField(max_length=66)

    def clean_group_name(self):
        g_name = self.cleaned_data.get('group_name')
        if ' ' in g_name:
            raise ValidationError("Do not use SPACE in you're group name")
        try:
            ChatGroup.objects.get(title=g_name)
            raise ValidationError('This name is already taken')
        except ChatGroup.DoesNotExist:
            return g_name
