import pytest
from datetime import date, timedelta
from decimal import Decimal
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.bookings.choices import BookingStatus
from apps.bookings.tests.booking_factory import BookingFactory
from apps.property.models import Property, Unit
from apps.property.tests.factories.property_factory import PropertyFactory
from apps.property.tests.factories.unit_factories import UnitFactory


def listings_list_url():
    return reverse('listings-list')


def listings_detail_url(property_uuid):
    return reverse('listings-detail', kwargs={'property_uuid': property_uuid})


@pytest.mark.django_db
class TestListingListAPIView:
    def test_list_is_public(self):
        prop = PropertyFactory(type=Property.Type.APARTMENT, status=Property.Status.ACTIVE)
        UnitFactory(property=prop, status=Unit.Status.AVAILABLE, price_per_night=Decimal('100'))

        client = APIClient()
        response = client.get(listings_list_url())

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_list_excludes_inactive_properties(self):
        active = PropertyFactory(status=Property.Status.ACTIVE)
        UnitFactory(property=active, status=Unit.Status.AVAILABLE)

        inactive = PropertyFactory(status=Property.Status.INACTIVE)
        UnitFactory(property=inactive, status=Unit.Status.AVAILABLE)

        client = APIClient()
        response = client.get(listings_list_url())

        assert response.status_code == status.HTTP_200_OK
        returned_uuids = {item['uuid'] for item in response.data}
        assert str(active.uuid) in returned_uuids
        assert str(inactive.uuid) not in returned_uuids

    def test_list_excludes_unavailable_units(self):
        prop = PropertyFactory(status=Property.Status.ACTIVE)
        UnitFactory(property=prop, status=Unit.Status.UNDER_MAINTENANCE)

        client = APIClient()
        response = client.get(listings_list_url())

        assert response.status_code == status.HTTP_200_OK
        returned_uuids = {item['uuid'] for item in response.data}
        assert str(prop.uuid) not in returned_uuids

    def test_list_filter_by_min_price(self):
        prop_cheap = PropertyFactory(status=Property.Status.ACTIVE)
        UnitFactory(property=prop_cheap, status=Unit.Status.AVAILABLE, price_per_night=Decimal('50'))

        prop_expensive = PropertyFactory(status=Property.Status.ACTIVE)
        UnitFactory(property=prop_expensive, status=Unit.Status.AVAILABLE, price_per_night=Decimal('300'))

        client = APIClient()
        response = client.get(listings_list_url(), {'min_price': 200})

        assert response.status_code == status.HTTP_200_OK
        returned_uuids = {item['uuid'] for item in response.data}
        assert str(prop_expensive.uuid) in returned_uuids
        assert str(prop_cheap.uuid) not in returned_uuids

    def test_list_filter_by_city(self):
        prop_berlin = PropertyFactory(status=Property.Status.ACTIVE, city='Berlin')
        UnitFactory(property=prop_berlin, status=Unit.Status.AVAILABLE)

        prop_paris = PropertyFactory(status=Property.Status.ACTIVE, city='Paris')
        UnitFactory(property=prop_paris, status=Unit.Status.AVAILABLE)

        client = APIClient()
        response = client.get(listings_list_url(), {'city': 'Berlin'})

        assert response.status_code == status.HTTP_200_OK
        returned_uuids = {item['uuid'] for item in response.data}
        assert str(prop_berlin.uuid) in returned_uuids
        assert str(prop_paris.uuid) not in returned_uuids

    def test_list_invalid_search_params(self):
        client = APIClient()

        response = client.get(listings_list_url(), {'check_in': 'not-a-date'})

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestListingDetailAPIView:
    def test_retrieve_active_property_is_public(self):
        prop = PropertyFactory(status=Property.Status.ACTIVE, type=Property.Type.APARTMENT)
        UnitFactory(property=prop, status=Unit.Status.AVAILABLE)

        client = APIClient()
        response = client.get(listings_detail_url(prop.uuid))

        assert response.status_code == status.HTTP_200_OK
        assert response.data['uuid'] == str(prop.uuid)

    def test_retrieve_inactive_property_returns_404(self):
        prop = PropertyFactory(status=Property.Status.INACTIVE)

        client = APIClient()
        response = client.get(listings_detail_url(prop.uuid))

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_retrieve_nonexistent_property_returns_404(self):
        import uuid

        client = APIClient()
        response = client.get(listings_detail_url(uuid.uuid4()))

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_retrieve_excludes_units_unavailable_for_dates(self):
        prop = PropertyFactory(status=Property.Status.ACTIVE, type=Property.Type.HOTEL)
        unit = UnitFactory(property=prop, status=Unit.Status.AVAILABLE, room_number='A1')
        check_in = date.today() + timedelta(days=5)
        check_out = date.today() + timedelta(days=10)
        BookingFactory(
            unit=unit,
            status=BookingStatus.CONFIRMED,
            check_in=check_in,
            check_out=check_out,
        )

        client = APIClient()
        response = client.get(
            listings_detail_url(prop.uuid),
            {'check_in': check_in.isoformat(), 'check_out': check_out.isoformat()},
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data['categories'] == []
