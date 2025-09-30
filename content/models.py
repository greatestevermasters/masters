from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import FileExtensionValidator
from django_summernote.fields import SummernoteTextField
from PIL import Image

from social.models import Comment, LikeDislike


# ---------- Helper ----------
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import FileExtensionValidator
from django_summernote.fields import SummernoteTextField
from PIL import Image

from social.models import Comment, LikeDislike


# ---------- Helper ----------
import os
import logging


class Post(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="content/")

    def __str__(self):
        return self.title

logger = logging.getLogger(__name__)

def compress_image(image_path: str) -> None:
    """
    Compress an image in-place while preserving the original file format.
    Works safely for .jpg/.jpeg and .png.
    """
    try:
        if not os.path.exists(image_path):
            logger.warning(f"compress_image: file not found: {image_path}")
            return

        ext = os.path.splitext(image_path)[1].lower()  # ".png" or ".jpg"
        with Image.open(image_path) as img:
            img_copy = img.copy()
            img_copy.thumbnail((1200, 1200))

            if ext in (".jpg", ".jpeg"):
                # ensure RGB (JPEG doesn't support alpha)
                if img_copy.mode in ("RGBA", "P", "LA"):
                    img_copy = img_copy.convert("RGB")
                img_copy.save(image_path, format="JPEG", quality=85, optimize=True)

            elif ext == ".png":
                # preserve alpha if present
                if img_copy.mode == "P":
                    img_copy = img_copy.convert("RGBA")
                img_copy.save(image_path, format="PNG", optimize=True)

            else:
                # fallback: save in detected format or overwrite
                fmt = img_copy.format or "PNG"
                try:
                    img_copy.save(image_path, format=fmt)
                except Exception:
                    img_copy.save(image_path)

    except Exception as e:
        logger.exception(f"compress_image error for {image_path}: {e}")
# ---------- Choices ----------
MASTER_CHOICES = [
    ("buddha", "Buddha"),
    ("osho", "Osho"),
    ("krishna", "Krishna"),
]

CONTENT_TYPE_CHOICES = [
    ("teaching", "Teaching"),
    ("book", "Book"),
    ("video", "Video"),
    ("blog", "Blog"),
]


# ---------- Abstract base ----------
class TimeStamped(models.Model):
    created = models.DateTimeField(default=timezone.now, editable=False)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created"]


# ---------- Unified model ----------
class Content(TimeStamped):
    """
    One model to handle every master (Buddha/Osho/Krishna) and
    every content type (Teaching/Book/Video/Blog).
    """
    master = models.CharField(max_length=20, choices=MASTER_CHOICES)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES)

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)

    # Generic text fields (Summernote for rich text)
    description = SummernoteTextField(blank=True)  # main body or long text
    excerpt = SummernoteTextField(blank=True)      # optional short intro (e.g. blog)

    # Optional fields used only for certain types
    url = models.URLField(blank=True, null=True)      # for video
    author = models.CharField(max_length=200, blank=True)  # for book

    # Additions for book buying links
    flipkart_buy_link = models.URLField(
        max_length=500,
        blank=True,
        null=True
    )

    amazon_buy_link = models.URLField(
        max_length=500,
        blank=True,
        null=True
    )

    image = models.ImageField(
        upload_to="content/%Y/%m/%d/",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"])],
    )

    # Social relations
    comments = GenericRelation(Comment, related_query_name="content_comments")
    likes = GenericRelation(LikeDislike, related_query_name="content_likes")

    class Meta:
        unique_together = ("master", "content_type", "slug")
        verbose_name = "Content Item"
        verbose_name_plural = "Content Items"

    def __str__(self) -> str:
        return f"{self.title} ({self.master} – {self.content_type})"

    def get_absolute_url(self):
        return reverse(
            "content:content_detail",
            kwargs={
                "master": self.master,
                "content_type": self.content_type,
                "slug": self.slug,
            },
        )

    # def save(self, *args, **kwargs):
    #     # Normalize YouTube links to embed format when type is video
    #     if self.content_type == "video" and self.url:
    #         if "youtube.com/watch?v=" in self.url:
    #             self.url = self.url.replace("watch?v=", "embed/")
    #         elif "youtu.be/" in self.url:
    #             video_id = self.url.split("/")[-1]
    #             self.url = f"https://www.youtube.com/embed/{video_id}"

    #     super().save(*args, **kwargs)

    #     # Compress image after save
    #     if self.image:
    #         compress_image(self.image.path)

def save(self, *args, **kwargs):
    # Normalize YouTube links (keep your existing logic)
    if self.content_type == "video" and self.url:
        if "youtube.com/watch?v=" in self.url:
            self.url = self.url.replace("watch?v=", "embed/")
        elif "youtu.be/" in self.url:
            video_id = self.url.split("/")[-1]
            self.url = f"https://www.youtube.com/embed/{video_id}"

    # Save first so ImageField file is written to disk
    super().save(*args, **kwargs)

    # Then compress the file on disk (safe: will not change extension)
    try:
        if self.image and getattr(self.image, "path", None):
            compress_image(self.image.path)
    except Exception as e:
        logger.exception(f"Error compressing image for Content(id={getattr(self, 'id', 'n/a')}): {e}")




# # ---------- Helper ----------
# def compress_image(image_path: str) -> None:
#     """Shrink uploaded images for better performance."""
#     img = Image.open(image_path)
#     img.thumbnail((1200, 1200))
#     if img.mode in ("RGBA", "P"):
#         img = img.convert("RGB")
#     img.save(image_path, format="JPEG", quality=80, optimize=True)


# # ---------- Choices ----------
# MASTER_CHOICES = [
#     ("buddha", "Buddha"),
#     ("osho", "Osho"),
#     ("krishna", "Krishna"),
# ]

# CONTENT_TYPE_CHOICES = [
#     ("teaching", "Teaching"),
#     ("book", "Book"),
#     ("video", "Video"),
#     ("blog", "Blog"),
# ]


# # ---------- Abstract base ----------
# class TimeStamped(models.Model):
#     created = models.DateTimeField(default=timezone.now, editable=False)
#     updated = models.DateTimeField(auto_now=True)

#     class Meta:
#         abstract = True
#         ordering = ["-created"]


# # ---------- Unified model ----------
# class Content(TimeStamped):
#     """
#     One model to handle every master (Buddha/Osho/Krishna) and
#     every content type (Teaching/Book/Video/Blog).
#     """
#     master = models.CharField(max_length=20, choices=MASTER_CHOICES)
#     content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES)

#     title = models.CharField(max_length=200)
#     slug = models.SlugField(max_length=220, unique=True)

#     # Generic text fields (Summernote for rich text)
#     description = SummernoteTextField(blank=True)  # main body or long text
#     excerpt = SummernoteTextField(blank=True)      # optional short intro (e.g. blog)

#     # Optional fields used only for certain types
#     url = models.URLField(blank=True, null=True)       # for video
#     author = models.CharField(max_length=200, blank=True)  # for book

#     image = models.ImageField(
#         upload_to="content/%Y/%m/%d/",
#         blank=True,
#         null=True,
#         validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"])],
#     )

#     # Social relations
#     comments = GenericRelation(Comment, related_query_name="content_comments")
#     likes = GenericRelation(LikeDislike, related_query_name="content_likes")

#     class Meta:
#         unique_together = ("master", "content_type", "slug")
#         verbose_name = "Content Item"
#         verbose_name_plural = "Content Items"

#     def __str__(self) -> str:
#         return f"{self.title} ({self.master} – {self.content_type})"

#     def get_absolute_url(self):
#         return reverse(
#             "content:content_detail",
#             kwargs={
#                 "master": self.master,
#                 "content_type": self.content_type,
#                 "slug": self.slug,
#             },
#         )

#     def save(self, *args, **kwargs):
#         # Normalize YouTube links to embed format when type is video
#         if self.content_type == "video" and self.url:
#             if "youtube.com/watch?v=" in self.url:
#                 self.url = self.url.replace("watch?v=", "embed/")
#             elif "youtu.be/" in self.url:
#                 video_id = self.url.split("/")[-1]
#                 self.url = f"https://www.youtube.com/embed/{video_id}"

#         super().save(*args, **kwargs)

#         # Compress image after save
#         if self.image:
#             compress_image(self.image.path)


# class Teaching(models.Model):
#     title = models.CharField(max_length=255)
#     master = models.ForeignKey('Master', on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='teachings/', null=True, blank=True)
#     excerpt = models.TextField(null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def get_absolute_url(self):
#         return f"/teachings/{self.id}/"

# class Book(models.Model):
#     title = models.CharField(max_length=255)
#     author = models.CharField(max_length=255, null=True, blank=True)
#     master = models.ForeignKey('Master', on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='books/', null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def get_absolute_url(self):
#         return f"/books/{self.id}/"

# class Video(models.Model):
#     title = models.CharField(max_length=255)
#     master = models.ForeignKey('Master', on_delete=models.CASCADE)
#     url = models.URLField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def get_absolute_url(self):
#         return f"/videos/{self.id}/"

# class Blog(models.Model):
#     title = models.CharField(max_length=255)
#     master = models.ForeignKey('Master', on_delete=models.CASCADE)
#     excerpt = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def get_absolute_url(self):
#         return f"/blogs/{self.id}/"


