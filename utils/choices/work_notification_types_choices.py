from django.db import models


class WorkNotificationType(models.TextChoices):
    UNREAD_COUNT = "unread_count", "Количество непрочитанных сообщений пользователя"
    CREATE = "work_create", "Создана задача на пользователя"
    UPDATE = "work_update", "Обновлена задача пользователя"
    UPDATE_STATUS = "work_status_update", "Обновлен статус задачи пользователя"
