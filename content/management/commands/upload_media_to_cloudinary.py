import os
from django.core.management.base import BaseCommand
from django.conf import settings
from content.models import Content
import cloudinary.uploader

class Command(BaseCommand):
    help = "Upload old media_backup images to Cloudinary"

    def handle(self, *args, **kwargs):
        base_path = os.path.join(settings.BASE_DIR, "media_backup")

        count = 0
        for post in Post.objects.all():
            if not post.image:
                continue

            image_path = os.path.join(base_path, post.image.name)

            if not os.path.exists(image_path):
                self.stdout.write(f"❌ Missing: {image_path}")
                continue

            result = cloudinary.uploader.upload(
                image_path,
                folder="content"
            )

            post.image = result["secure_url"]
            post.save()
            count += 1

            self.stdout.write(f"✅ Uploaded: {post.image}")

        self.stdout.write(self.style.SUCCESS(f"\nDONE. Uploaded {count} images"))
