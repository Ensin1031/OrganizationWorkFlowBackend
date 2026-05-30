from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from notifications.services.notification_service import NotificationService
from utils.choices.work_notification_types_choices import WorkNotificationType
from work.models.work import Work


@receiver(post_save, sender=Work)
def work_saved(sender, instance, created, **kwargs):
    user = instance.execute_by
    if not user:
        return
    if created:
        NotificationService.send(
            user=user,
            notification_type=str(WorkNotificationType.CREATE.value),
            title='Новая задача',
            message=f'Вам назначена задача <a href="/home/tasks/{instance.slug}" '
                    f'target="_blank" rel="noopener noreferrer">{instance.full_name()}</a>',
            payload={
                'type': 'work_created',
                'work_id': instance.id,
            }
        )


@receiver(pre_save, sender=Work)
def work_status_changed(sender, instance: Work, **kwargs):
    if not instance.pk:
        return
    user = instance.execute_by
    if not user:
        return
    old: Work = Work.objects.get(pk=instance.pk)
    link = f'<a href="/home/tasks/{instance.slug}" target="_blank" rel="noopener noreferrer">{instance.full_name()}</a>'

    if old.status_id != instance.status_id:
        NotificationService.send(
            user=user,
            notification_type=str(WorkNotificationType.UPDATE_STATUS.value),
            title='Изменение статуса задачи',
            message=(
                f'Задача "{link}" '
                f'переведена в статус "{instance.status.status.name}"'
            ),
            payload={
                'type': 'status_changed',
                'work_slug': instance.slug,
                'project_status_id': instance.status_id,
                'status_id': instance.status.status_id,
                'status_name': instance.status.status.name,
            }
        )
    elif old.execute_by_id != instance.execute_by_id:
        if old.execute_by:
            NotificationService.send(
                user=old.execute_by,
                notification_type=str(WorkNotificationType.UPDATE.value),
                title='Изменен исполнитель задачи',
                message=(
                    f'Задаче "{link}" '
                    f'назначен новый исполнитель "{instance.execute_by.get_full_name()}"'
                ),
                payload={
                    'type': WorkNotificationType.UPDATE.value,
                    'work_slug': instance.slug,
                }
            )
        NotificationService.send(
            user=user,
            notification_type=str(WorkNotificationType.UPDATE.value),
            title='Изменен исполнитель задачи',
            message=f'Вам назначена задача "{link}"',
            payload={
                'type': WorkNotificationType.UPDATE.value,
                'work_slug': instance.slug,
            }
        )
    else:
        NotificationService.send(
            user=user,
            notification_type=str(WorkNotificationType.UPDATE.value),
            title='Задача изменена',
            message=f'Изменена задача "{link}"',
            payload={
                'type': WorkNotificationType.UPDATE.value,
                'work_slug': instance.slug,
            }
        )
