import random

import factory

from users.models import UserExtended


class UserExtendedFactory(factory.django.DjangoModelFactory):
    """
    Фабрика для создания пользователей
    """

    class Meta:
        model = UserExtended

    is_superuser = False
    username = factory.Sequence(lambda n: 'user-test-{}'.format(factory.Faker("first_name_male")))
    first_name = factory.Faker('first_name_male', locale='ru_Ru')
    last_name = factory.Faker('last_name_male', locale='ru_Ru')
    second_name = factory.Faker('middle_name', locale='ru_Ru')
    # Переделал генерацию email - добавил случайные числа и sequence
    # чтобы исключить дубликаты и спорадические падения тестов
    email = factory.Sequence(lambda n: f"x{str(random.randint(1, 5000))}x{n}x" +
                                       factory.Faker("email").evaluate(None, None, {'locale': 'RU'}))
    is_staff = False
    is_active = True

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        password = kwargs.pop("password", None)
        obj = super(UserExtendedFactory, cls)._create(model_class, *args, **kwargs)
        obj.set_password(password)
        obj.save()
        return obj

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        self.groups.add(*extracted)
