
from django import template
import bleach

register = template.Library()

@register.filter(name="clean_html")
def clean_html(value):
    # Allow paragraph and basic formatting tags
    allowed_tags = ['p', 'br', 'strong', 'b', 'em', 'i', 'u']
    return bleach.clean(value or "", tags=allowed_tags, strip=True)
