#!/usr/bin/python3
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


#used to automatically create a profile when a user is created
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

#used to save the profile to database
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save() #Instance is the user
