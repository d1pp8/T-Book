import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from apps.bookings.choices import BookingStatus
from apps.bookings.tests.booking_factory import BookingFactory
from apps.property.tests.factories.unit_factories import UnitFactory
from apps.users.tests.user_factory import UserFactory
from apps.reviews.tests.review_factory import ReviewFactory


@pytest.mark.django_db
def test_get_review_list():
    user = UserFactory()
    client = APIClient()
    client.force_authenticate(user)
    ReviewFactory(user=user)
    url = reverse('reviews:list-create-review')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_review_list_unauthorized():
    client = APIClient()
    url = reverse('reviews:list-create-review')
    response = client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_get_empty_review_list():
    user = UserFactory()
    client = APIClient()
    client.force_authenticate(user)
    url = reverse('reviews:list-create-review')
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 0


@pytest.mark.django_db
def test_get_only_own_reviews():
    user = UserFactory()
    another_user = UserFactory()
    ReviewFactory(user=user)
    ReviewFactory(user=another_user)
    client = APIClient()
    client.force_authenticate(user)
    url = reverse('reviews:list-create-review')
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data['results']) == 1


@pytest.mark.django_db
def test_create_review_success():
    user = UserFactory()
    unit = UnitFactory()

    booking = BookingFactory(
        user=user,
        unit=unit,
        status=BookingStatus.COMPLETED,
    )

    client = APIClient()
    client.force_authenticate(user)
    url = reverse('reviews:list-create-review')

    data = {
        "booking": str(booking.uuid),
        "rating": 5,
        "comment": "Excellent!"
    }

    response = client.post(url, data=data, format="json")

    assert response.status_code == status.HTTP_201_CREATED