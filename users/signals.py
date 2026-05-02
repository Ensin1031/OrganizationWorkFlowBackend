from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import UserExtended


@receiver(post_save, sender=UserExtended)
def user_saved(sender, instance: UserExtended, created, **kwargs):

    pass
