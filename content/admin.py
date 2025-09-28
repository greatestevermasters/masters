from django.contrib import admin
from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Content


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
