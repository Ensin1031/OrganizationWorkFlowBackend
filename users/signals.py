import random

from django.core.files.base import ContentFile
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from users.models import UserExtended
from utils.generate_random_avatar_svg import generate_avatar_svg


@receiver(post_save, sender=UserExtended)
def user_saved(sender, instance: UserExtended, created, **kwargs):

    pass


@receiver(pre_save, sender=UserExtended)
def user_pre_saved(sender, instance: UserExtended, **kwargs):

    if not getattr(instance.profile_photo, 'name', ''):
        svg = generate_avatar_svg(user=instance)

        filename = f'user_avatar_{instance.slug or random.randint(1000, 999999)}.svg'

        instance.profile_photo.save(
            filename,
            ContentFile(svg.encode('utf-8')),
            save=False,
        )
