from django import template
from django.forms.widgets import Textarea
register = template.Library()

@register.filter(name='add_class')
def add_class(value, css_class):
    return value.as_widget(attrs={'class': css_class})


@register.filter
def is_textarea(field):
    return isinstance(field.field.widget, Textarea)