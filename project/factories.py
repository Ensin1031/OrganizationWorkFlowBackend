import factory
from factory.django import DjangoModelFactory

from project.models import Project, ProjectStatus, ProjectVersion, ProjectCategory, ProjectType
from references.factories import StatusRowFactory
from users.factories import UserExtendedFactory


class ProjectCategoryFactory(DjangoModelFactory):
    """ Фабрика для модели ProjectCategory """

    class Meta:
        model = ProjectCategory
        django_get_or_create = ('name',)

    name = factory.Sequence(lambda n: f'Проект {n}')


class ProjectTypeFactory(DjangoModelFactory):
    """ Фабрика для модели ProjectType """

    class Meta:
        model = ProjectType
        django_get_or_create = ('name',)

    name = factory.Sequence(lambda n: f'Проект {n}')


class ProjectFactory(DjangoModelFactory):
    """ Фабрика для модели Project """

    class Meta:
        model = Project
        django_get_or_create = ('name',)

    name = factory.Sequence(lambda n: f'Проект {n}')
    manage_by = factory.SubFactory(UserExtendedFactory)
    category = factory.SubFactory(ProjectCategoryFactory)
    type = factory.SubFactory(ProjectTypeFactory)


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
