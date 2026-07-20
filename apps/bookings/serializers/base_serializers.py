from rest_framework import serializers

from apps.bookings.choices import BookingStatus
from apps.bookings.models import Booking
from apps.bookings.services import BookingService
from apps.property.models import Unit, Property
from apps.property.serializers import UnitDetailSerializer


class BookingCreateSerializer(serializers.Serializer):
    unit = serializers.SlugRelatedField(slug_field="uuid", queryset=Unit.objects.all())
    check_in = serializers.DateField()
    check_out = serializers.DateField()
    adults = serializers.IntegerField(min_value=1)
    children = serializers.IntegerField(min_value=0)
    special_request = serializers.CharField(required=False, allow_blank=True)


class BookingListSerializer(serializers.ModelSerializer):
    property_title = serializers.CharField(source='unit.property.title')
    property_type = serializers.CharField(source='unit.property.type')
    unit_title = serializers.CharField(source='unit.title')
    number_of_guests = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = [
            'uuid',
            'status',
            'check_in',
            'check_out',
            'number_of_guests',
            'total_price',
            'property_title',
            'property_type',
            'unit_title'
        ]

    def get_number_of_guests(self, obj: Booking) -> int:
        return obj.adults + obj.children


class BookingPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = [
            'uuid',
            'title',
            'city',
            'country',
            'street',
            'house_number',
            'postal_code',
            'floor'
        ]


class BookingDetailSerializer(serializers.ModelSerializer):
    unit = UnitDetailSerializer(read_only=True)
    property = BookingPropertySerializer(source='unit.property', read_only=True)
    duration = serializers.SerializerMethodField()
    can_cancel = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = [
            'uuid',
            'status',
            'property',
            'unit',
            'check_in',
            'check_out',
            'adults',
            'children',
            'price_per_night',
            'total_price',
            'special_request',
            'duration',
            'can_cancel'
        ]

    def get_duration(self, obj: Booking):
        return (obj.check_out - obj.check_in).days

    def get_can_cancel(self, obj: Booking):
        return (
                obj.status in (
            BookingStatus.PENDING,
            BookingStatus.CONFIRMED
        )
                and BookingService._is_cancellation_allowed(obj)
        )
