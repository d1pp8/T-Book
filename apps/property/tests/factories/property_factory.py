import factory

from apps.property.models import Property
from apps.users.tests.user_factory import UserFactory


class PropertyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Property

    owner = factory.SubFactory(UserFactory)
    title = 'Apartment in Berlin'
    description = 'Very cool Apartment'
    country = 'Germany'
    city = 'Berlin'
    street = 'Berliner Allee'
    house_number = factory.sequence(lambda n: f'1{n}A')
    postal_code = '12345'
    floor = 1

