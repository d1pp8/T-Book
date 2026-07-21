from django.urls import path

from .views.property_image_views import (
    PropertyImageUploadAPIView,
    PropertyImageDeleteAPIView,
    PropertyImageSetCoverAPIView,
    PropertyImageSetOrderAPIView,
)

from .views.unit_image_views import (
    UnitImageUploadAPIView,
    UnitImageDeleteAPIView,
    UnitImageSetCoverAPIView,
    UnitImageSetOrderAPIView,
)

app_name = 'media'


urlpatterns = [

    path("<uuid:property_uuid>/images/", PropertyImageUploadAPIView.as_view(),name="property-image-upload"),
    path("<uuid:property_uuid>/images/<uuid:property_image_uuid>/", PropertyImageDeleteAPIView.as_view(), name="property-image-delete"),
    path("<uuid:property_uuid>/images/<uuid:property_image_uuid>/cover/",PropertyImageSetCoverAPIView.as_view(), name="property-image-set-cover"),
    path("<uuid:property_uuid>/images/ordering/", PropertyImageSetOrderAPIView.as_view(), name="property-image-set-order"),


    path("<uuid:property_uuid>/units/<uuid:unit_uuid>/images/", UnitImageUploadAPIView.as_view(), name="unit-image-upload"),
    path("<uuid:property_uuid>/units/<uuid:unit_uuid>/images/<uuid:unit_image_uuid>/", UnitImageDeleteAPIView.as_view(), name="unit-image-delete"),
    path("<uuid:property_uuid>/units/<uuid:unit_uuid>/images/<uuid:unit_image_uuid>/cover/", UnitImageSetCoverAPIView.as_view(), name="unit-image-set-cover"),
    path("<uuid:property_uuid>/units/<uuid:unit_uuid>/images/ordering/",UnitImageSetOrderAPIView.as_view(), name="unit-image-set-order"),
]