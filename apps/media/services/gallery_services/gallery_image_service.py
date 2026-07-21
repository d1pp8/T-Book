from pathlib import Path
from PIL import Image

from django.db import transaction
from django.db.models import Max
from django.core.files.uploadedfile import UploadedFile

from apps.common.mixins import MediaOwnerMixin
from apps.media.models import Media
from apps.media.validators import MediaValidator

import logging

logger = logging.getLogger(__name__)


class GalleryImageService:
    image_model = None
    owner_field = None


    @classmethod
    def upload_many(cls, owner: MediaOwnerMixin, uploaded_files):
        images = []
        with transaction.atomic():
            for uploaded_file in uploaded_files:
                images.append(cls.upload(owner=owner, uploaded_file=uploaded_file))

        return images


    @classmethod
    def upload(cls, owner: MediaOwnerMixin, uploaded_file: UploadedFile):
        MediaValidator.validate(uploaded_file)
        metadata = cls._extract_metadata(uploaded_file)

        with transaction.atomic():
            media = Media(**metadata)
            path = cls._build_upload_path(owner, media, uploaded_file)

            media.file.save(name=path, content=uploaded_file, save=False,)
            media.save()

            return cls.image_model.objects.create(
                **{
                    cls.owner_field: owner,
                    "media": media,
                    "is_cover": cls._is_first_image(owner),
                    "ordering": cls._get_next_ordering(owner),
                }
            )


    @classmethod
    def delete(cls, image):
        owner = getattr(image, cls.owner_field)

        media = image.media
        file = media.file

        with transaction.atomic():
            if image.is_cover and owner.images.count() > 1:
                cls._set_next_cover(owner, image)
            media.delete()

        try:
            file.delete(save=False)
        except Exception:
            logger.exception(f"Failed to delete file - {file.name}")


    @classmethod
    def set_cover(cls, image):
        owner = getattr(image, cls.owner_field)

        with transaction.atomic():
            cls._set_cover(image, owner.images.all())

        return image


    @classmethod
    def reorder(cls, owner, validated_data):
        with transaction.atomic():
            images = owner.images.all()
            reordered = cls._set_new_order(images, validated_data)

            cls.image_model.objects.bulk_update(
                reordered,
                fields=["ordering"],
            )




    @staticmethod
    def _extract_metadata(uploaded_file):
        try:
            with Image.open(uploaded_file) as image:
                width = image.width
                height = image.height
        finally:
            uploaded_file.seek(0)

        return {
            'original_name': uploaded_file.name,
            'mime_type': uploaded_file.content_type,
            'size': uploaded_file.size,
            'width': width,
            'height': height,
        }


    @staticmethod
    def _build_upload_path(owner, media, uploaded_file):
        extension = Path(uploaded_file.name).suffix.lower()

        return (
            f"{owner.MEDIA_FOLDER}/"
            f"{owner.uuid}/"
            f"{media.uuid}{extension}"
        )


    @staticmethod
    def _is_first_image(owner):
        return not owner.images.exists()


    @staticmethod
    def _get_next_ordering(owner):
        max_ordering = owner.images.aggregate(Max("ordering"))["ordering__max"]
        if max_ordering is None:
            return 0
        return max_ordering + 1

    @staticmethod
    def _set_cover(image, images):
        images.update(is_cover=False)
        image.is_cover = True
        image.save(update_fields=["is_cover"])

    @classmethod
    def _set_next_cover(cls, owner, deleted_image):
        next_cover = (owner.images.exclude(pk=deleted_image.pk).order_by("ordering").first())
        if next_cover:
            cls._set_cover(next_cover, owner.images.all())

    @staticmethod
    def _set_new_order(images, validated_data):
        image_map = {
            image.uuid: image
            for image in images
        }
        for item in validated_data:
            image_map[item["uuid"]].ordering = item["ordering"]
        return list(image_map.values())