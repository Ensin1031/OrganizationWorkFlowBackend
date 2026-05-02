import random
from datetime import date, timedelta

import factory
from factory.django import DjangoModelFactory

from sprint.models import Sprint


class SprintFactory(DjangoModelFactory):
    """ Фабрика для модели Sprint """

    class Meta:
        model = Sprint
        django_get_or_create = ('name',)

    name = factory.Sequence(lambda n: f'Спринт {n}')

    start_date = factory.LazyFunction(lambda: date.today() + timedelta(days=random.randint(-30, 30)))
    end_date = factory.LazyAttribute(lambda obj: obj.start_date + timedelta(days=random.randint(7, 30)))

    description = factory.Faker('sentence', nb_words=10)
