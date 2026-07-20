import django_filters
from django.db.models import Q

from apps.property.models import Property, Unit


class ListingFilter(django_filters.FilterSet):

    ordering = django_filters.OrderingFilter(
        fields = [
            ('price_per_night', 'price'),
            ('created_at', 'created'),
        ]
    )

    # Units
    bedrooms = django_filters.NumberFilter(field_name='bedrooms', lookup_expr='gte')
    bathrooms = django_filters.NumberFilter(field_name='bathrooms', lookup_expr='gte')

    # amenities = django_filters.
    # beds = django_filters.NumberFilter(field_name='beds', lookup_expr='gte')

    max_area = django_filters.NumberFilter(field_name='area', lookup_expr="lte")
    min_area = django_filters.NumberFilter(field_name='area', lookup_expr="gte")

    max_price = django_filters.NumberFilter(field_name='price_per_night', lookup_expr="lte", )
    min_price = django_filters.NumberFilter(field_name='price_per_night', lookup_expr="gte")

    guests = django_filters.NumberFilter(field_name='max_guests', lookup_expr="gte")


    # Property
    search = django_filters.CharFilter(method='filter_search')
    type = django_filters.ChoiceFilter(field_name='property__type', choices=Property.Type.choices)
    country = django_filters.CharFilter(field_name='property__country', lookup_expr='istartswith')
    city = django_filters.CharFilter(field_name='property__city', lookup_expr='icontains')
    min_rating = django_filters.NumberFilter(field_name='property__rating', lookup_expr='gte')


    class Meta:
        model = Unit
        fields = [
            'bedrooms',
            'bathrooms',
            'max_area',
            'min_area',
            'max_price',
            'min_price',
            'guests',
            'search',
            'type',
            'country',
            'city',
            'min_rating',
            'ordering'
        ]

    def filter_search(self, queryset, name, value):
        return queryset.filter(Q(property__title__icontains=value)| Q(property__description__icontains=value))