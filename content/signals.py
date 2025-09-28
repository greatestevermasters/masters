from django.db.models.signals import post_save
from django.dispatch import receiver
from django_summernote.models import Attachment
from PIL import Image
import os

@receiver(post_save, sender=Attachment)
def compress_summernote_image(sender, instance, **kwargs):
    """
    Automatically compress any image uploaded via Summernote.
    Works for every Content entry (Buddha, Osho, Krishna) without duplication.
    """
    if not instance.file:
        return

    try:
        # Only process image files (skip PDFs, etc.)
        ext = os.path.splitext(instance.file.name)[1].lower()
        if ext not in [".jpg", ".jpeg", ".png"]:
            return

        image_path = instance.file.path
        img = Image.open(image_path)

        # Convert to RGB if needed (prevents errors on PNG with alpha)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        # Resize if larger than 1200x1200 while keeping aspect ratio
        max_size = (1200, 1200)
        img.thumbnail(max_size)

        # Save as optimized JPEG with 80% quality
        img.save(image_path, format="JPEG", quality=80, optimize=True)

    except Exception as e:
        # Don’t raise—just log if something goes wrong
        print(f"Image compression failed: {e}")
