import pytest
from apps.property.models import Amenity

@pytest.mark.django_db
def test_amenity_str():
    amenity = Amenity.objects.create(title='Wi-Fi')
    assert str(amenity) == 'Wi-Fi'