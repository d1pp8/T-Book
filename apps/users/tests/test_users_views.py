import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.users.models import User
from apps.users.tests.user_factory import UserFactory


def register_url():
    return reverse('users:register')


def login_url():
    return reverse('users:login')


def token_refresh_url():
    return reverse('users:token_refresh')


def profile_url():
    return reverse('users:profile')


def change_password_url():
    return reverse('users:change_password')


@pytest.mark.django_db
class TestRegisterView:
    def test_register_success(self):
        client = APIClient()
        payload = {
            'email': 'newuser@example.com',
            'password': 'StrongPass123!',
            'password2': 'StrongPass123!',
            'first_name': 'Jane',
            'last_name': 'Doe',
        }

        response = client.post(register_url(), data=payload, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        user = User.objects.get(email='newuser@example.com')
        assert user.check_password('StrongPass123!')

    def test_register_password_mismatch(self):
        client = APIClient()
        payload = {
            'email': 'newuser@example.com',
            'password': 'StrongPass123!',
            'password2': 'DifferentPass123!',
            'first_name': 'Jane',
            'last_name': 'Doe',
        }

        response = client.post(register_url(), data=payload, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert not User.objects.filter(email='newuser@example.com').exists()

    def test_register_duplicate_email_fails(self):
        UserFactory(email='taken@example.com')
        client = APIClient()
        payload = {
            'email': 'taken@example.com',
            'password': 'StrongPass123!',
            'password2': 'StrongPass123!',
            'first_name': 'Jane',
            'last_name': 'Doe',
        }

        response = client.post(register_url(), data=payload, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data

    def test_register_weak_password_fails(self):
        client = APIClient()
        payload = {
            'email': 'newuser@example.com',
            'password': '123',
            'password2': '123',
            'first_name': 'Jane',
            'last_name': 'Doe',
        }

        response = client.post(register_url(), data=payload, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestLoginView:
    def test_login_success(self):
        user = UserFactory(email='login@example.com')
        client = APIClient()

        response = client.post(
            login_url(),
            data={'email': 'login@example.com', 'password': 'Qwerty123!'},
            format='json',
        )

        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data
        assert response.data['user']['email'] == user.email

    def test_login_wrong_password(self):
        UserFactory(email='login@example.com')
        client = APIClient()

        response = client.post(
            login_url(),
            data={'email': 'login@example.com', 'password': 'WrongPass!'},
            format='json',
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_missing_fields(self):
        client = APIClient()

        response = client.post(login_url(), data={'email': 'login@example.com'}, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_login_nonexistent_user(self):
        client = APIClient()

        response = client.post(
            login_url(),
            data={'email': 'ghost@example.com', 'password': 'Whatever123!'},
            format='json',
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestTokenRefreshView:
    def test_refresh_token_success(self):
        user = UserFactory(email='refresh@example.com')
        client = APIClient()
        login_response = client.post(
            login_url(),
            data={'email': 'refresh@example.com', 'password': 'Qwerty123!'},
            format='json',
        )
        refresh_token = login_response.data['refresh']

        response = client.post(token_refresh_url(), data={'refresh': refresh_token}, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data

    def test_refresh_token_invalid(self):
        client = APIClient()

        response = client.post(token_refresh_url(), data={'refresh': 'invalid-token'}, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestProfileView:
    def test_get_profile_unauthorized(self):
        client = APIClient()

        response = client.get(profile_url())

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_profile_success(self):
        user = UserFactory(first_name='Alice')
        client = APIClient()
        client.force_authenticate(user)

        response = client.get(profile_url())

        assert response.status_code == status.HTTP_200_OK
        assert response.data['email'] == user.email
        assert response.data['first_name'] == 'Alice'

    def test_update_profile_success(self):
        user = UserFactory(first_name='Alice')
        client = APIClient()
        client.force_authenticate(user)

        response = client.patch(profile_url(), data={'first_name': 'Alicia'}, format='json')

        assert response.status_code == status.HTTP_200_OK
        user.refresh_from_db()
        assert user.first_name == 'Alicia'


@pytest.mark.django_db
class TestChangePasswordView:
    def test_change_password_success(self):
        user = UserFactory()
        client = APIClient()
        client.force_authenticate(user)

        response = client.post(
            change_password_url(),
            data={
                'old_password': 'Qwerty123!',
                'new_password': 'NewStrongPass456!',
                'new_password2': 'NewStrongPass456!',
            },
            format='json',
        )

        assert response.status_code == status.HTTP_200_OK
        user.refresh_from_db()
        assert user.check_password('NewStrongPass456!')

    def test_change_password_wrong_old_password(self):
        user = UserFactory()
        client = APIClient()
        client.force_authenticate(user)

        response = client.post(
            change_password_url(),
            data={
                'old_password': 'WrongOldPass!',
                'new_password': 'NewStrongPass456!',
                'new_password2': 'NewStrongPass456!',
            },
            format='json',
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_change_password_mismatch(self):
        user = UserFactory()
        client = APIClient()
        client.force_authenticate(user)

        response = client.post(
            change_password_url(),
            data={
                'old_password': 'Qwerty123!',
                'new_password': 'NewStrongPass456!',
                'new_password2': 'DifferentPass456!',
            },
            format='json',
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_change_password_unauthorized(self):
        client = APIClient()

        response = client.post(
            change_password_url(),
            data={
                'old_password': 'Qwerty123!',
                'new_password': 'NewStrongPass456!',
                'new_password2': 'NewStrongPass456!',
            },
            format='json',
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
