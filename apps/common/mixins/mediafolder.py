

class MediaOwnerMixin:
    @property
    def media_folder(self) -> str:
        raise NotImplementedError