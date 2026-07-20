import factory
from apps.users.models import User

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n:f'user{n}@gmail.com')
    password = factory.PostGenerationMethodCall('set_password', 'Qwerty123!')
    