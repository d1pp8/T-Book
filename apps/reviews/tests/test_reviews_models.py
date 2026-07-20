import pytest

from apps.reviews.tests.review_factory import ReviewFactory


@pytest.mark.django_db
def test_review_str():
    review = ReviewFactory(rating=8)

    assert str(review) == f"{review.property.title} ({review.rating}/10)"