from apps.media.models import PropertyImage
from apps.media.services.gallery_services.gallery_image_service import GalleryImageService


class PropertyImageService(GalleryImageService):
    image_model = PropertyImage
    owner_field = 'property'