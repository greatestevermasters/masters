from django.contrib import admin
from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Content

from django.contrib import admin
# from .models import Post   # add more models here if needed

# @admin.register(Post)
# class PostAdmin(admin.ModelAdmin):
#     list_display = ("id", "title")   # fields you want visible in admin list
#     search_fields = ("title",)


class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = "__all__"
        widgets = {
            "description": SummernoteWidget(),
            "excerpt": SummernoteWidget(),
        }


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    form = ContentForm
    list_display = ("title", "master", "content_type", "created")
    list_filter = ("master", "content_type", "created")
    search_fields = ("title", "description", "excerpt")
    prepopulated_fields = {"slug": ("title",)}
