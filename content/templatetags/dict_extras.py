from django import template

register = template.Library()
@register.filter
def dict_get(value, key):
    """
    Safely get a key from a dictionary.
    Returns an empty list if value is not a dict or key not found.
    """
    if not isinstance(value, dict):
        return []
    return value.get(key, [])

