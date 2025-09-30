import os
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()


# ✅ Configure Cloudinary using CLOUDINARY_URL
cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True,
)

# 🔹 Path to your local media folder
MEDIA_DIR = os.path.join(os.getcwd(), "media")

def upload_media():
    for root, dirs, files in os.walk(MEDIA_DIR):
        for file in files:
            file_path = os.path.join(root, file)

            # Keep folder structure (e.g. "content/...")
            relative_path = os.path.relpath(file_path, MEDIA_DIR).replace("\\", "/")

            print(f"Uploading {relative_path}...")

            cloudinary.uploader.upload(
                file_path,
                folder=os.path.dirname(relative_path),  # e.g. "content/"
                public_id=os.path.splitext(os.path.basename(file))[0],  # filename without extension
                overwrite=True
            )

    print("✅ All media files uploaded to Cloudinary!")

if __name__ == "__main__":
    upload_media()
