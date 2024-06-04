#!/usr/bin/python3
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image #for image processing

def user_directory_path(instance, filename):
    '''Used to make a unique location for each user's
       property file handling location'''
    ext = filename.split('.')[-1]
    new_filename = f"{instance.user.username}_{timezone.now}.{ext}"
    return f'user_{instance.user.id}/profile_pic/{new_filename}'

class Region(models.Model):
    """A region model for user/requests profile"""
    region = models.CharField(max_length=45, unique=True)
    details = models.TextField()
    updated_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True) #can not be modified

    def __str__(self) -> str:
        return f'{self.region}'
    
class City(models.Model):
    """A city model for user/requests profile"""
    city = models.CharField(max_length=45, unique=True)
    details = models.TextField(blank=True)
    updated_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True) #can not be modified

    def __str__(self) -> str:
        return f'{self.city}'

class SubCity(models.Model):
    """A subcity model for user/requests profile"""
    subcity = models.CharField(max_length=45, unique=True)
    details = models.TextField(blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='subcities')
    updated_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True) #can not be modified

    def __str__(self) -> str:
        return f'{self.subcity}'
    



class Profile(models.Model):
    """A model used for additional user informations"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default="common/avatar.png", upload_to=user_directory_path)
    mobile = models.CharField(max_length=20)
    optional_mobile = models.CharField(max_length=20, blank=True)
    #profile should not be deleted if region is deleted
    region = models.ForeignKey(Region, default=None,
                               null=True, on_delete=models.SET_NULL)
    city = models.ForeignKey(City, default=None, null=True,
                             on_delete=models.SET_NULL)
    subcity = models.ForeignKey(SubCity, default=None, null=True,
                             on_delete=models.SET_NULL)
    address = models.CharField(max_length=120, blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True) #can not be modified


    def save(self,  *args, **kwargs):
        '''used for processing image before saving to the database'''
        super(Profile, self).save(*args, **kwargs)
        img = Image.open(self.avatar.path)

        if img.height > 300 or img.width > 300:
            outpt = (300, 300)
            img.thumbnail(outpt)
            img.save(self.avatar.path)
    def __str__(self) -> str:
        return f"{self.user.username}'s Profile"
