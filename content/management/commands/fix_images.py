import os
from django.core.management.base import BaseCommand
from content.models import Content
from PIL import Image

class Command(BaseCommand):
    help = "Re-compress and fix broken images (especially PNGs) for Content model."

    def handle(self, *args, **kwargs):
        fixed = 0
        skipped = 0

        for obj in Content.objects.exclude(image=""):
            img_path = obj.image.path
            if not os.path.exists(img_path):
                self.stdout.write(self.style.WARNING(f"Missing file: {img_path}"))
                continue

            try:
                # Open and re-save properly
                img = Image.open(img_path)
                img.thumbnail((1200, 1200))

                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")

                ext = img_path.split(".")[-1].lower()

                if ext in ["jpg", "jpeg"]:
                    img.save(img_path, format="JPEG", quality=80, optimize=True)
                elif ext == "png":
                    img.save(img_path, format="PNG", optimize=True)
                else:
                    img.save(img_path)

                fixed += 1
                self.stdout.write(self.style.SUCCESS(f"Fixed: {img_path}"))

            except Exception as e:
                skipped += 1
                self.stdout.write(self.style.ERROR(f"Error fixing {img_path}: {e}"))

        self.stdout.write(self.style.SUCCESS(f"✅ Done! Fixed {fixed} images, skipped {skipped}."))
