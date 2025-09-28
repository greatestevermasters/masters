from django import template
import re

register = template.Library()

@register.filter
def youtube_id(value):
    """
    Extracts the YouTube video ID from a URL or returns the ID if already provided.
    """
    if not value:
        return ""
    
    # Match full YouTube URLs
    regex = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/watch\?v=|youtu\.be\/)([A-Za-z0-9_-]{11})"
    match = re.search(regex, value)
    if match:
        return match.group(1)
    
    # If value itself is a valid 11-character YouTube ID
    if re.match(r'^[A-Za-z0-9_-]{11}$', value):
        return value
    
    return value  # fallback, return original if nothing matches

@register.filter
def youtube_embed_url(value):
    """
    Converts a YouTube URL or ID into a full embed URL using the privacy-enhanced 'nocookie' domain.
    """
    video_id = youtube_id(value)
    if video_id and re.match(r'^[A-Za-z0-9_-]{11}$', video_id):
        # Use the privacy-enhanced embed URL
        return f'https://www.youtube-nocookie.com/embed/{video_id}'
    
    return value  # fallback if ID is invalid
