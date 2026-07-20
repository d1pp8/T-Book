from django.urls import path

from apps.property.views.property_views import (
    PropertyListCreateAPIView,
    PropertyRetrieveUpdateDestroyAPIView,
)
from apps.property.views.unit_views import (
    UnitListCreateAPIView,
    UnitRetrieveUpdateDestroyAPIView
)
from apps.property.views.amenity_views import AmenityListAPIView
from apps.property.views.bed_views import BedTypeChoicesAPIView


app_name = 'property'

urlpatterns = [
    path('', PropertyListCreateAPIView.as_view(), name='property-list-create',),
    path('<uuid:property_uuid>/', PropertyRetrieveUpdateDestroyAPIView.as_view(), name='property-detail-update-delete',),

    path('<uuid:property_uuid>/units/', UnitListCreateAPIView.as_view(), name='unit-list-create',),
    path('<uuid:property_uuid>/units/<uuid:unit_uuid>/', UnitRetrieveUpdateDestroyAPIView.as_view(), name='unit-detail-update-delete',),


    # Catalogs
    path('amenities/', AmenityListAPIView.as_view(), name='amenities-list'),
    path('beds/types/', BedTypeChoicesAPIView.as_view(), name='bed-types'),
]