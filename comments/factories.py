import factory
from factory.django import DjangoModelFactory

from comments.models import WorkComment
from users.factories import UserExtendedFactory
from work.factories import WorkFactory


class WorkCommentFactory(DjangoModelFactory):
    """ Фабрика для модели WorkComment """

    class Meta:
        model = WorkComment
        django_get_or_create = ('created_by', 'work')

    created_by = factory.SubFactory(UserExtendedFactory)
    work = factory.SubFactory(WorkFactory)

    description = factory.Faker('sentence', nb_words=10)
