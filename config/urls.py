from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/property/', include('apps.property.urls')),
    path('api/v1/media/', include('apps.media.urls')),

    path('api/v1/users/', include('apps.users.urls')),
    path('api/v1/listings/', include('apps.listings.urls')),

    path('api/v1/owner/bookings/', include('apps.bookings.urls.owner_urls')),
    path('api/v1/bookings/', include('apps.bookings.urls.user_urls')),

    path('api/v1/reviews/', include('apps.reviews.urls')),
]


urlpatterns += [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
