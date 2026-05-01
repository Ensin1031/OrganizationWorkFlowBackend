from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower

from utils.model_mixins import CreatedUpdatedMixin


class UserExtended(CreatedUpdatedMixin, AbstractUser):
    """ Пользователь (расширенная модель) """
    username = models.CharField("Имя пользователя", db_index=True, max_length=255, unique=True)
    email = models.EmailField("E-mail", db_index=True, unique=True)
    second_name = models.CharField("Отчество", max_length=255, blank=True)
    is_active = models.BooleanField("Активен", default=True)
    is_staff = models.BooleanField("Персонал", default=False)

    is_verified = models.BooleanField(
        "Верифицирован", default=False,
        help_text="Указывает, завершил ли данный пользователь"
                  " процесс проверки электронной почты, чтобы разрешить вход в систему")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["-id", ]

        constraints = [
            UniqueConstraint(
                Lower("email"),
                name="user_email_ci_uniqueness",
            ),
        ]

    def __str__(self):
        return self.username

    def get_full_name(self):
        return self._get_full_name() if self._has_full_name() else self._get_default_name()

    def get_short_name(self):
        return self.username

    def _has_full_name(self) -> bool:
        return not self._get_full_name().isspace()

    def _get_full_name(self) -> str:
        return f"{self.last_name} {self.first_name} {self.second_name}"

    def _get_default_name(self) -> str:
        return "Пользователь без имени"
