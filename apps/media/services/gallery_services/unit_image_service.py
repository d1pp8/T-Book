from rest_framework.validators import ValidationError

from apps.property.models import Unit
from apps.media.models import UnitImage
from apps.media.services.gallery_services.gallery_image_service import GalleryImageService



class UnitImageService(GalleryImageService):
    image_model = UnitImage
    owner_field = "unit"

    @staticmethod
    def validate_images_allowed(unit: Unit):
        if unit.property.is_single_unit:
            raise ValidationError(f"Images for '{unit.property.type.upper()}' should be attached to Property.")