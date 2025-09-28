# content/templatetags/custom_filters.py
from django import template
import re

register = template.Library()

@register.filter
def strip_outer_p(value):
    """Remove all wrapping <p> tags from the string"""
    if value:
        # Remove any number of <p> at start and </p> at end
        return re.sub(r'^(\s*<p>)+', '', re.sub(r'(</p>\s*)+$', '', value))
    return value
