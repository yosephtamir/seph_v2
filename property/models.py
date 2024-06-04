from django.db import models
import os
from seph_v2 import settings
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from user.models import SubCity



def user_directory_path(instance, filename):
    '''Used to make a unique location for each user's
       property file handling location'''
    ext = filename.split('.')[-1]
    new_filename = f"{instance.property.user.username}_{timezone.now()}.{ext}"
    return f'user_{instance.property.user.id}/property/{new_filename}'


class Category(models.Model):
    '''Available categories model for property'''
    category = models.CharField(max_length=128)
    details = models.TextField(blank=True)
    updated_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True) #can not be modified

    def __str__(self) -> str:
        return f'{self.category}'



class PropertyPost(models.Model):
    """A property representation"""
    property = models.CharField(max_length=128, null=False)
    price = models.FloatField(null=False)
    kare = models.FloatField(null=False)
    details = models.TextField(null=False)
    subcity = models.ForeignKey(SubCity, null=True, on_delete=models.SET_NULL)
    address = models.TextField(null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    rented = models.BooleanField(default=False)
    updated_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True) #can not be modified

    def delete(self, *args, **kwargs):
        images = self.images.all()
        for image in images:
            if image.image:
                image_path = os.path.join(settings.MEDIA_ROOT, image.image.name)
                if os.path.isfile(image_path):
                    os.remove(image_path)
        super(PropertyPost, self).delete(*args, **kwargs)

    def get_first_image(self):
        return self.images.first()
    
    def __str__(self) -> str:
        return f'({self.id}) {self.property}'
    
    def get_absolute_url(self):
        '''used to redirect to requestion detail'''
        return reverse("propertydetails", kwargs={"pk": self.pk})
    

class PropertyImage(models.Model):
    '''A property representation images model'''
    image = models.ImageField(upload_to=user_directory_path)
    property = models.ForeignKey(PropertyPost, related_name="images", on_delete=models.CASCADE)
    updated_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True) #can not be modified

    def __str__(self) -> str:
        return f"({self.id}) {self.property}'s image"
    
