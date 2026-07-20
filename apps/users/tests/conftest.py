import pytest
from apps.users.models import User
from apps.users.tests.user_factory import UserFactory


@pytest.fixture
def user():
    return UserFactory()

@pytest.fixture
def super_user():
    return User.objects.create_superuser(
        email='test@gmail.com',
        password='Qwerty123!'
    )