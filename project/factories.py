import factory
from factory.django import DjangoModelFactory

from project.models import Project, ProjectStatus, ProjectVersion
from references.factories import StatusRowFactory


class ProjectFactory(DjangoModelFactory):
    """ Фабрика для модели Project """

    class Meta:
        model = Project
        django_get_or_create = ('name',)

    name = factory.Sequence(lambda n: f'Проект {n}')


class ProjectStatusFactory(DjangoModelFactory):
    """ Фабрика для модели ProjectStatus """

    class Meta:
        model = ProjectStatus
        django_get_or_create = ('project', 'status')

    project = factory.SubFactory(ProjectFactory)
    status = factory.SubFactory(StatusRowFactory)


class ProjectVersionFactory(DjangoModelFactory):
    """Фабрика для модели ProjectVersion (стадия/версия проекта)"""

    class Meta:
        model = ProjectVersion

    # Связь с проектом
    project = factory.SubFactory(ProjectFactory)

    name = factory.Sequence(lambda n: f'Версия {n}')
