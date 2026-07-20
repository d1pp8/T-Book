
from apps.property.models import (
    Property,
    Unit,
)

from apps.media.serializers import (
    PropertyImageSerializer,
    UnitImageSerializer,
)
from apps.property.serializers.amenity_serializers import AmenitySerializer

class ContentSourceMixin:
    def _content_source(self, unit: Unit) -> Property | Unit:
        if unit.property.is_single_unit:
            return unit.property
        return unit

    def _get_image_serializer(self, source: Property | Unit):
        if isinstance(source, Property):
            return PropertyImageSerializer
        return UnitImageSerializer

    def get_title(self, obj: Unit):
        return self._content_source(obj).title

    def get_description(self, obj: Unit):
        return self._content_source(obj).description

    def get_images(self, obj: Unit):
        source = self._content_source(obj)
        serializer = self._get_image_serializer(source)
        return serializer(source.images.all(), many=True, context=self.context).data

    def get_amenities(self, obj: Unit):
        source = self._content_source(obj)
        return AmenitySerializer(source.amenities.all(),many=True,context=self.context,).data