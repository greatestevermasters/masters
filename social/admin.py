from django.contrib import admin
from .models import Comment, LikeDislike

admin.site.register(Comment)
admin.site.register(LikeDislike)
