from .models import Property
import django_filters

class PropertyFilter(django_filters.FilterSet):

    type = django_filters.ChoiceFilter(field_name='type', choices=Property.Type.choices)
    status = django_filters.ChoiceFilter(field_name='status', choices=Property.Status.choices)

    country = django_filters.CharFilter(field_name='country', lookup_expr='istartswith')
    city = django_filters.CharFilter(field_name='city', lookup_expr='icontains')

    min_rating = django_filters.NumberFilter(field_name='rating', lookup_expr='gte')

    min_price = django_filters.NumberFilter(field_name='min_price',lookup_expr="gte",)
    max_guests = django_filters.NumberFilter(field_name='max_guests', lookup_expr="lte", )

    # amentities но там другая модель она у меня пока не реализована и как с ManyToMany быть без понятия

    class Meta:
        model = Property
        fields = [
            'type',
            'status',
            'country',
            'city',
            'min_rating',
        ]


