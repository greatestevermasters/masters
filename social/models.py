from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class TimeStamped(models.Model):
    created = models.DateTimeField(default=timezone.now, editable=False)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created"]

class LikeDislike(TimeStamped):
    LIKE = 1
    DISLIKE = -1
    VALUE_CHOICES = ((LIKE, "Like"), (DISLIKE, "Dislike"))

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    value = models.SmallIntegerField(choices=VALUE_CHOICES)

    class Meta:
        unique_together = ("user", "content_type", "object_id")

class Comment(TimeStamped):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    text = models.TextField()

# class Share(TimeStamped):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shares')
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForeignKey("content_type", "object_id")
#     platform = models.CharField(max_length=50, default="link")

# Assuming you already have a TimeStamped base class
class Share(TimeStamped):
    PLATFORM_CHOICES = [
        ("whatsapp", "WhatsApp"),
        ("gmail", "Gmail"),
        ("facebook", "Facebook"),
        ("twitter", "Twitter"),
        ("instagram", "Instagram"),
        ("linkedin", "LinkedIn"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shares')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    platform = models.CharField(
        max_length=50,
        choices=PLATFORM_CHOICES,
        default="whatsapp",
    )

    def __str__(self):
        return f"{self.user} shared on {self.platform}"