from django.contrib import admin
from .models import Comment, LikeDislike, Share

admin.site.register(Comment)
admin.site.register(LikeDislike)
admin.site.register(Share)
