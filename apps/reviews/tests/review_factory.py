import factory

from apps.reviews.models import Review
from apps.bookings.choices import BookingStatus
from apps.bookings.tests.booking_factory import BookingFactory


class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Review

    booking = factory.SubFactory(BookingFactory,status=BookingStatus.COMPLETED)

    user = factory.SelfAttribute('booking.user')
    property = factory.SelfAttribute('booking.unit.property')
    rating = 8
    comment = factory.Faker('sentence')