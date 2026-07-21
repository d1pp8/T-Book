from rest_framework import serializers

from apps.bookings.choices import BookingStatus
from apps.bookings.models import Booking
from apps.bookings.services import BookingService
from apps.property.models import Unit, Property
from apps.property.serializers import UnitDetailSerializer


class BookingCreateSerializer(serializers.Serializer):
    unit = serializers.SlugRelatedField(
        slug_field='uuid',
        queryset=Unit.objects.all(),
        help_text='UUID of the unit to be booked.'
    )
    check_in = serializers.DateField(help_text='Check-in date in YYYY-MM-DD format.')
    check_out = serializers.DateField(help_text='Check-out date in YYYY-MM-DD format.')
    adults = serializers.IntegerField(
        min_value=1,
        help_text='Number of adult guests.'
    )
    children = serializers.IntegerField(
        min_value=0,
        help_text='Number of child guests.'
    )
    special_request = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text='Optional message for the property owner.'
    )



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
    duration = serializers.SerializerMethodField(help_text='Booking duration in nights.')
    can_cancel = serializers.SerializerMethodField(help_text='Indicates whether the booking can still be cancelled.')

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
