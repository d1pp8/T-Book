from django.db import transaction

from apps.users.models import User
from apps.property.models import Property
from apps.bookings.models import Booking

from apps.reviews.models import Review
from apps.reviews.validators import ReviewValidator

from django.db.models import Avg, Count
from django.db import transaction


class ReviewService:
    @classmethod
    def create(cls, user: User, booking: Booking, rating:int, comment:str = "") -> Review:
        with transaction.atomic():
            ReviewValidator.validate_owner(user, booking)
            ReviewValidator.validate_completed(booking)
            ReviewValidator.validate_review_exists(booking)
            review = Review.objects.create(
                user=user,
                booking=booking,
                property=booking.unit.property,
                rating=rating,
                comment=comment
            )
            cls._update_property_rating(review.property)
        return review


    @classmethod
    def update(cls, user, review: Review, **data) -> Review:
        ReviewValidator.validate_owner(user=user, booking=review.booking)

        if 'rating' in data:
            review.rating = data['rating']
        if 'comment' in data:
            review.comment = data['comment']
        with transaction.atomic():
            review.save(update_fields=['rating', 'comment'])
            cls._update_property_rating(review.property)

        return review

    @classmethod
    def delete(cls, user, review: Review) -> None:
        ReviewValidator.validate_owner(user=user, booking=review.booking)
        prop = review.property
        with transaction.atomic():
            review.delete()
            cls._update_property_rating(prop)


    @classmethod
    def _update_property_rating(cls, prop: Property) -> None:
        stats = (
            Review.objects
            .filter(property=prop)
            .aggregate(avg=Avg('rating'),count=Count('id'))
        )
        prop.rating = stats['avg'] or 0
        prop.review_count = stats['count']
        prop.save(update_fields = ['rating','review_count'])