import factory

from users.models import UserExtended


class UserExtendedFactory(factory.django.DjangoModelFactory):
    """ Фабрика для создания пользователей """

    class Meta:
        model = UserExtended

    is_superuser = False
    username = factory.Sequence(lambda n: f'user-test-{n}')
    first_name = factory.Faker('first_name_male', locale='ru_Ru')
    last_name = factory.Faker('last_name_male', locale='ru_Ru')
    second_name = factory.Faker('middle_name', locale='ru_Ru')
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    is_staff = False
    is_active = True

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        password = kwargs.pop("password", "password123")
        obj = super()._create(model_class, *args, **kwargs)
        obj.set_password(password)
        obj.save(update_fields=["password"])
        return obj

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        self.groups.add(*extracted)
