import os
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils.text import slugify
from content.models import Content

class Command(BaseCommand):
    help = "Recover posts from media_backup/content folder"

    def handle(self, *args, **kwargs):
        base_dir = os.path.join(settings.BASE_DIR, "media_backup", "content")

        if not os.path.exists(base_dir):
            self.stdout.write(self.style.ERROR("❌ media_backup/content not found"))
            return

        created = 0

        for root, dirs, files in os.walk(base_dir):
            for file in files:
                if not file.lower().endswith((".jpg", ".jpeg", ".png")):
                    continue

                full_path = os.path.join(root, file)

                title = os.path.splitext(file)[0].replace("_", " ").title()
                slug = slugify(title)

                if Content.objects.filter(slug=slug).exists():
                    continue

                post = Content.objects.create(
                    master="buddha",       # change if needed
                    content_type="blog",   # change if needed
                    title=title,
                    slug=slug,
                )

                with open(full_path, "rb") as f:
                    post.image.save(file, f, save=True)

                created += 1
                self.stdout.write(f"✅ Recovered: {title}")

        self.stdout.write(self.style.SUCCESS(f"\n🎉 DONE: {created} posts recovered"))
