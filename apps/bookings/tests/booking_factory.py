import factory
from decimal import Decimal
from datetime import date, timedelta

from apps.bookings.models import Booking
from apps.bookings.choices import BookingStatus

from apps.property.tests.factories.unit_factories import UnitFactory
from apps.users.tests.user_factory import UserFactory


class BookingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Booking

    user = factory.SubFactory(UserFactory)
    unit = factory.SubFactory(UnitFactory)

    status = BookingStatus.PENDING
    adults = 2
    children = 0

    check_in = date.today()
    check_out = date.today() + timedelta(days=5)
    price_per_night = Decimal('100')
    total_price = Decimal('300')

    special_request = ''