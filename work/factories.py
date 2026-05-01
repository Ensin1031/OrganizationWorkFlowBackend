import random
from datetime import timedelta

import factory
from django.utils import timezone
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyDateTime, FuzzyChoice

from project.factories import ProjectStatusFactory, ProjectFactory
from references.factories import WorkTypeFactory, WorkDifficultyFactory, WorkTechnologyFactory, WorkPriorityFactory
from sprint.factories import SprintFactory
from users.factories import UserExtendedFactory
from utils.choices.work_connection_choices import WorkConnectionType
from work.models.work import Work
from work.models.work_connection import WorkConnection


class WorkFactory(DjangoModelFactory):
    """Фабрика для модели Work """

    class Meta:
        model = Work

    name = factory.Sequence(lambda n: f'Работа {n}')
    priority = factory.SubFactory(WorkPriorityFactory)
    project = factory.SubFactory(ProjectFactory)
    status = factory.SubFactory(ProjectStatusFactory)
    created_by = factory.SubFactory(UserExtendedFactory)

    description = factory.Faker('text', max_nb_chars=200)

    epic = None
    type = factory.SubFactory(WorkTypeFactory)
    sprint = factory.SubFactory(SprintFactory)
    execute_by = None
    difficulty = factory.SubFactory(WorkDifficultyFactory)
    technology = factory.SubFactory(WorkTechnologyFactory)

    histories = factory.List([])
    tags = factory.List([])
    versions = factory.List([])

    target_start_date = FuzzyDateTime(
        start_dt=timezone.now() - timedelta(days=30),
        end_dt=timezone.now() + timedelta(days=30)
    )
    target_end_date = FuzzyDateTime(
        start_dt=timezone.now() + timedelta(days=1),
        end_dt=timezone.now() + timedelta(days=60)
    )

    lead_time = factory.LazyFunction(lambda: timedelta(hours=random.randint(1, 40)))
    wasted_time = factory.LazyFunction(lambda: timedelta(hours=random.randint(0, 10)))

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Переопределение для корректной работы slug (модель требует двух сохранений)."""
        # Убираем ManyToMany из kwargs, так как они добавляются после создания объекта
        m2m_fields = ['histories', 'tags', 'versions']
        m2m_data = {field: kwargs.pop(field, []) for field in m2m_fields if field in kwargs}

        obj = model_class(*args, **kwargs)
        obj.save()

        if not obj.slug:
            obj.slug = f"{obj.project.code_prefix}-{obj.pk}".upper()
            obj.save(update_fields=['slug'])

        # Добавляем ManyToMany связи
        for field_name, values in m2m_data.items():
            getattr(obj, field_name).set(values)

        return obj


class WorkConnectionFactory(DjangoModelFactory):
    """Фабрика для модели WorkConnection """

    class Meta:
        model = WorkConnection

    type = FuzzyChoice(WorkConnectionType.values)

    work_from = factory.SubFactory(WorkFactory)
    work_to = factory.SubFactory(WorkFactory)
