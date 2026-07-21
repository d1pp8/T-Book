from rest_framework import serializers



class BedSerializer(serializers.Serializer):
    type = serializers.CharField()
    quantity = serializers.IntegerField()


class ListingCardSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    type = serializers.CharField(max_length=20)
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    cover_image = serializers.CharField(allow_null=True)
    country = serializers.CharField(max_length=30)
    city = serializers.CharField(max_length=30)
    rating = serializers.DecimalField(max_digits=4, decimal_places=2, min_value=0, max_value=10)
    review_count = serializers.IntegerField(min_value=0)
    price_from = serializers.DecimalField(max_digits=10, decimal_places=2,)
    guests_to = serializers.IntegerField(max_value=15)
    beds = serializers.IntegerField(min_value=0)


class AddressSerializer(serializers.Serializer):
    country = serializers.CharField()
    city = serializers.CharField()
    street = serializers.CharField()
    house_number = serializers.CharField()
    postal_code = serializers.CharField()


class OwnerSerializer(serializers.Serializer):
    name = serializers.CharField()
    avatar = serializers.CharField(allow_null=True)


class AmenitySerializer(serializers.Serializer):
    title = serializers.CharField()
    icon = serializers.CharField(allow_null=True)


class RoomCategorySerializer(serializers.Serializer):
    unit_uuid = serializers.UUIDField()
    title = serializers.CharField()
    description = serializers.CharField()
    amenities = AmenitySerializer(many=True)
    gallery = serializers.ListField(child=serializers.CharField())
    price_from = serializers.DecimalField(max_digits=10, decimal_places=2)
    price_to = serializers.DecimalField(max_digits=10, decimal_places=2)
    area_from = serializers.IntegerField(min_value=5)
    area_to = serializers.IntegerField(min_value=5)
    guests_from = serializers.IntegerField(min_value=1)
    guests_to = serializers.IntegerField(min_value=1)
    beds = BedSerializer(many=True)
    units_available = serializers.IntegerField()



class ReviewSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    user = serializers.CharField()
    rating = serializers.IntegerField()
    comment = serializers.CharField()
    created_at = serializers.DateTimeField()



class ListingDetailSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()

    owner = OwnerSerializer()
    type = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    amenities = AmenitySerializer(many=True)
    address = AddressSerializer()
    gallery = serializers.ListField(child=serializers.CharField())

    rating = serializers.DecimalField(max_digits=4, decimal_places=2)
    review_count = serializers.IntegerField(min_value=0)
    reviews = ReviewSerializer(many=True)

    unit_uuid = serializers.UUIDField(allow_null=True)
    price_per_night = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        allow_null=True,
    )
    area = serializers.IntegerField(allow_null=True)
    bedrooms = serializers.IntegerField(allow_null=True)
    bathrooms = serializers.IntegerField(allow_null=True)
    max_guests = serializers.IntegerField(allow_null=True)
    beds = BedSerializer(many=True, allow_null=True)
    categories = RoomCategorySerializer(many=True)




class ListingSearchSerializer(serializers.Serializer):
    check_in = serializers.DateField(required=False)
    check_out = serializers.DateField(required=False)

    adults = serializers.IntegerField(required=False)
    children = serializers.IntegerField(required=False)