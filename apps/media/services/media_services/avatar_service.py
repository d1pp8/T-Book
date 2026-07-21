from apps.media.models import UserAvatar
from apps.media.services.media_services.media_service import MediaService


class UserAvatarService(MediaService):
    image_model = UserAvatar
    owner_field = 'avatar'