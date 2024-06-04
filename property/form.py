#!/usr/bin/python3
"""A user related forms for mathod based views"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import modelformset_factory

from .models import PropertyPost, PropertyImage
from user.models import City, SubCity


class PropertyPostForm(forms.ModelForm):
    '''a form user registration view and model'''
    city = forms.ModelChoiceField(queryset=City.objects.all(), required=True, label="City")

    class Meta:
        model = PropertyPost
        fields = ['property', 'price', 'kare', 'details', 'city', 'subcity', 'address', 'category']
        widgets = {
            'details': forms.Textarea(attrs={'rows': 1, 'placeholder': 'Type a detail description of your property...'}),
            'address': forms.Textarea(attrs={'rows': 1, 'placeholder': 'Type address of your property...'}),
            'kare': forms.Textarea(attrs={'rows': 1, 'placeholder': 'Type area of your property in kare meter...'}),
            'property': forms.Textarea(attrs={'rows': 1, 'placeholder': 'Type a title of your property...'}),
            'price': forms.Textarea(attrs={'rows': 1, 'placeholder': 'Type a rental price per month of property...'}),


        }

    def __init__(self, *args, **kwargs):
        super(PropertyPostForm, self).__init__(*args, **kwargs)
        if 'city' in self.data:
            try:
                city_id = int(self.data.get('city'))
                self.fields['subcity'].queryset = SubCity.objects.filter(city_id=city_id).order_by('subcity')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['subcity'].queryset = self.instance.subcity.city.subcities.order_by('subcity')
        else:
            self.fields['subcity'].queryset = SubCity.objects.none()
    
class PropertyImageForm(forms.ModelForm):
    '''A form for image upload view and model'''
    class Meta:
        model = PropertyImage
        fields = ['image']

PropertyImageFormSet = modelformset_factory(
    PropertyImage, form=PropertyImageForm, extra=3, can_delete=True
)