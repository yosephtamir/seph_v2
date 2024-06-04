#!/usr/bin/python3.8
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView
from django.contrib import messages
from .form import (UserRegisterForm, ProfileUpdateForm, 
                    UserUpdateForm)
from property.models import PropertyPost
from django.contrib.auth.models import User


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html', {'form': form})

@login_required
def profile(request):

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('Home')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        curr_user = request.user
        myproperties = PropertyPost.objects.filter(user=curr_user).all()
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'myproperties': myproperties,
        'profile': True,
        'title': f"{request.user.first_name}"
    }

    return render(request, 'user/profile.html', context)


class UserProfile(DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'user/user_profile.html'

