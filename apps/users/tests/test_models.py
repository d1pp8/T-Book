import pytest
from django.db import IntegrityError
from apps.users.models import User
from apps.users.tests.user_factory import UserFactory


@pytest.mark.django_db
def test_user_can_be_created(user):
    saved_user = User.objects.get(pk=user.pk)
    assert saved_user.email == user.email
    assert User.objects.count() == 1
    assert user == saved_user


@pytest.mark.django_db
def test_user_password_is_hashed(user):
    saved_user = User.objects.get(pk=user.pk)
    assert saved_user.password != 'Qwerty123!'
    assert saved_user.check_password('Qwerty123!')


@pytest.mark.django_db
def test_user_email_must_be_unique(user):
    with pytest.raises(IntegrityError):
        User.objects.create_user(
            email=user.email,
            password='Qwerty123!'
        )


@pytest.mark.django_db
def test_superuser_can_be_created(super_user):
    saved_superuser = User.objects.get(pk=super_user.pk)
    assert saved_superuser.is_staff
    assert saved_superuser.is_superuser
    assert saved_superuser.check_password('Qwerty123!')



@pytest.mark.django_db
def test_amenity_str():
    user = UserFactory()
    assert str(user) == user.email