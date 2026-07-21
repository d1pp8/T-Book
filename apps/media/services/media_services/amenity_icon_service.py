from apps.media.models import AmenityIcon
from apps.media.services.media_services.media_service import MediaService


class AmenityIconService(MediaService):
    image_model = AmenityIcon
    owner_field = 'amenity'