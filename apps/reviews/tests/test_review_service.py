import pytest

from apps.reviews.models import Review
from apps.reviews.services import ReviewService
from apps.reviews.tests.review_factory import ReviewFactory
from apps.reviews.exceptions import ReviewOwnershipError

from apps.users.tests.user_factory import UserFactory

from apps.bookings.choices import BookingStatus
from apps.reviews.exceptions import BookingNotCompleted
from apps.bookings.tests.booking_factory import BookingFactory



@pytest.mark.django_db
def test_create_review():
    booking = BookingFactory(status=BookingStatus.COMPLETED,)

    review = ReviewService.create(
        user=booking.user,
        booking=booking,
        rating=9,
        comment='Excellent',
    )

    assert Review.objects.count() == 1
    assert review.user == booking.user
    assert review.booking == booking
    assert review.property == booking.unit.property
    assert review.rating == 9


@pytest.mark.django_db
def test_property_rating_after_create():
    booking = BookingFactory(status=BookingStatus.COMPLETED,)
    ReviewService.create(
        user=booking.user,
        booking=booking,
        rating=7,
    )

    booking.unit.property.refresh_from_db()

    assert booking.unit.property.rating == 7
    assert booking.unit.property.review_count == 1


@pytest.mark.django_db
def test_update_review():
    review = ReviewFactory()

    ReviewService.update(
        user=review.user,
        review=review,
        rating=10,
        comment='Updated',
    )
    review.refresh_from_db()

    assert review.rating == 10
    assert review.comment == 'Updated'


@pytest.mark.django_db
def test_property_rating_after_update():
    review = ReviewFactory(rating=6)
    ReviewService.update(
        user=review.user,
        review=review,
        rating=10,
    )
    review.property.refresh_from_db()

    assert review.property.rating == 10


@pytest.mark.django_db
def test_delete_review():
    review = ReviewFactory()
    ReviewService.delete(user=review.user, review=review)

    assert Review.objects.count() == 0


@pytest.mark.django_db
def test_property_rating_after_delete():
    review = ReviewFactory(rating=8)
    prop = review.property
    ReviewService.delete(user=review.user, review=review)
    prop.refresh_from_db()

    assert prop.rating == 0
    assert prop.review_count == 0


@pytest.mark.django_db
def test_create_review_for_not_completed_booking():
    booking = BookingFactory(status=BookingStatus.CONFIRMED)

    with pytest.raises(BookingNotCompleted):
        ReviewService.create(
            user=booking.user,
            booking=booking,
            rating=8,
        )


import pytest

from apps.reviews.exceptions import ReviewAlreadyExist


@pytest.mark.django_db
def test_create_second_review():
    booking = BookingFactory(status=BookingStatus.COMPLETED)

    ReviewFactory(
        booking=booking,
        user=booking.user,
        property=booking.unit.property,
    )

    with pytest.raises(ReviewAlreadyExist):
        ReviewService.create(
            user=booking.user,
            booking=booking,
            rating=9,
        )

import pytest

from apps.reviews.exceptions import ReviewAlreadyExist


@pytest.mark.django_db
def test_create_second_review():
    booking = BookingFactory(status=BookingStatus.COMPLETED)

    ReviewFactory(
        booking=booking,
        user=booking.user,
        property=booking.unit.property,
    )

    with pytest.raises(ReviewAlreadyExist):
        ReviewService.create(
            user=booking.user,
            booking=booking,
            rating=9,
        )


@pytest.mark.django_db
def test_create_review_by_another_user():
    booking = BookingFactory(status=BookingStatus.COMPLETED)
    another_user = UserFactory()

    with pytest.raises(ReviewOwnershipError):
        ReviewService.create(
            user=another_user,
            booking=booking,
            rating=8,
        )


@pytest.mark.django_db
def test_update_by_another_user():
    review = ReviewFactory()
    another_user = UserFactory()

    with pytest.raises(ReviewOwnershipError):
        ReviewService.update(
            user=another_user,
            review=review,
            rating=10,
        )

@pytest.mark.django_db
def test_delete_by_another_user():
    review = ReviewFactory()

    another_user = UserFactory()

    with pytest.raises(ReviewOwnershipError):
        ReviewService.delete(
            user=another_user,
            review=review,
        )