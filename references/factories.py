import factory
from factory.django import DjangoModelFactory

from references.models.status import StatusRow
from references.models.work_difficulty import WorkDifficulty
from references.models.work_priority import WorkPriority
from references.models.work_tag import WorkTag
from references.models.work_technology import WorkTechnology
from references.models.work_type import WorkType


class WorkTagFactory(DjangoModelFactory):
    """ Фабрика для модели WorkTag """

    class Meta:
        model = WorkTag

    name = factory.Sequence(lambda n: f'Тег {n}')


class StatusRowFactory(DjangoModelFactory):
    """ Фабрика для модели StatusRow """

    class Meta:
        model = StatusRow

    name = factory.Sequence(lambda n: f'Статус {n}')


class WorkTechnologyFactory(DjangoModelFactory):
    """ Фабрика для модели WorkTechnology """

    class Meta:
        model = WorkTechnology

    name = factory.Sequence(lambda n: f'Технология {n}')


class WorkDifficultyFactory(DjangoModelFactory):
    """ Фабрика для модели WorkDifficulty """

    class Meta:
        model = WorkDifficulty

    name = factory.Sequence(lambda n: f'Уровень {n}')


class WorkPriorityFactory(DjangoModelFactory):
    """ Фабрика для модели WorkPriority """

    class Meta:
        model = WorkPriority

    name = factory.Sequence(lambda n: f'Приоритет {n}')


class WorkTypeFactory(DjangoModelFactory):
    """ Фабрика для модели WorkType """

    class Meta:
        model = WorkType

    id = factory.Sequence(lambda n: n + 10)
    name = factory.Sequence(lambda n: f'Тип работы {n}')
