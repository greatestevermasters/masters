from django import template
from django.template.loader import render_to_string

register = template.Library()

@register.simple_tag(takes_context=True)
def social_buttons(context, obj, prev_url=None, next_url=None):
    user = context['request'].user
    return render_to_string('social/social_buttons.html', {
        'object': obj,
        'user': user,
        'prev_url': prev_url,
        'next_url': next_url,
        'request': context['request']
    })
