from django.core.files.uploadedfile import UploadedFile
from rest_framework.exceptions import ValidationError
from django.conf import settings

from PIL import Image, UnidentifiedImageError

from pathlib import Path

class MediaValidator:

    @staticmethod
    def validate(uploaded_file: UploadedFile) -> None:
        MediaValidator._validate_size(uploaded_file)
        MediaValidator._validate_extension(uploaded_file)
        MediaValidator._validate_content_type(uploaded_file)
        MediaValidator._validate_image(uploaded_file)


    @staticmethod
    def _validate_size(uploaded_file):
        if uploaded_file.size > settings.MEDIA_MAX_UPLOAD_SIZE:
            raise ValidationError("Image size exceeds the maximum allowed size.")


    @staticmethod
    def _validate_extension(uploaded_file):
        if Path(uploaded_file.name).suffix.lower() not in settings.MEDIA_ALLOWED_EXTENSIONS:
            raise ValidationError("Unsupported file extension.")


    @staticmethod
    def _validate_content_type(uploaded_file):
        if uploaded_file.content_type not in settings.MEDIA_ALLOWED_MIME_TYPES:
            raise ValidationError("Unsupported MIME type.")


    @staticmethod
    def _validate_image(uploaded_file):
        try:
            with Image.open(uploaded_file) as image:
                image.verify()
        except (UnidentifiedImageError, OSError):
            raise ValidationError("Uploaded file is not a valid image.")
        finally:
            uploaded_file.seek(0)
