from django import template
from django.forms.widgets import CheckboxInput


register = template.Library()
@register.filter(name='add_class')
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})
