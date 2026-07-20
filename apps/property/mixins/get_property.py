from rest_framework.generics import get_object_or_404


class PropertyLookupMixin:
    def get_property(self):
        from apps.property.models import Property
        return get_object_or_404(
            Property.objects.filter(owner=self.request.user),
            uuid=self.kwargs['property_uuid'],
        )