from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    """Check if a user belongs to a specific group."""
    if user.is_authenticated:
        return user.groups.filter(name=group_name).exists()
    return False
