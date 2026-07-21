from pathlib import Path
from PIL import Image

from django.db import transaction
from django.core.files.uploadedfile import UploadedFile

from apps.common.mixins import MediaOwnerMixin
from apps.media.models import Media
from apps.media.validators import MediaValidator

import logging

logger = logging.getLogger(__name__)


class MediaService:
    image_model = None
    owner_field = None


    @classmethod
    def upload(cls, owner: MediaOwnerMixin, uploaded_file: UploadedFile):
        MediaValidator.validate(uploaded_file)
        metadata = cls._extract_metadata(uploaded_file)

        with transaction.atomic():
            media = Media(**metadata)
            path = cls._build_upload_path(owner, media, uploaded_file)

            media.file.save(name=path, content=uploaded_file, save=False,)
            media.save()

            return cls.image_model.objects.create(**{cls.owner_field: owner,'media': media})


    @classmethod
    def delete(cls, image):
        owner = getattr(image, cls.owner_field)

        media = image.media
        file = media.file

        try:
            file.delete(save=False)
        except Exception:
            logger.exception(f"Failed to delete file - {file.name}")



    @staticmethod
    def _extract_metadata(uploaded_file):
        try:
            with Image.open(uploaded_file) as image:
                width = image.width
                height = image.height
        finally:
            uploaded_file.seek(0)

        return {
            "original_name": uploaded_file.name,
            "mime_type": uploaded_file.content_type,
            "size": uploaded_file.size,
            "width": width,
            "height": height,
        }


    @staticmethod
    def _build_upload_path(owner, media, uploaded_file):
        extension = Path(uploaded_file.name).suffix.lower()
        return (
            f"{owner.MEDIA_FOLDER}/"
            f"{media.uuid}{extension}"
        )