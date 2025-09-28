from django.contrib import admin
from .models import Content

@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ("title", "master", "content_type", "created")  # ✅ use created
    list_filter = ("master", "content_type", "created")
    search_fields = ("title", "description", "excerpt")
    prepopulated_fields = {"slug": ("title",)}
