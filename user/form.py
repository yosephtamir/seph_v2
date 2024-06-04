#!/usr/bin/python3
"""A user related forms for mathod based views"""
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    '''a form user registration view and model'''
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    '''A form for user update view and model'''
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    '''A form for profile update view and model'''
    class Meta:
        model = Profile
        fields = ['avatar', 'region', 'city', 'subcity', 'address', 'mobile', 'optional_mobile']
