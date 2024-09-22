from django import template
from django.forms.widgets import Textarea
register = template.Library()

@register.filter(name='add_class')
def add_class(value, css_class):
    return value.as_widget(attrs={'class': css_class})


@register.filter
def is_textarea(field):
    return isinstance(field.field.widget, Textarea)





@register.filter
def range_filter(value):
    """Returns a list of integers from 0 to value-1, with default handling for None."""
    if value is None:
        return []
    try:
        value = int(value)  # Ensure value is an integer
        return range(value)
    except ValueError:
        return []