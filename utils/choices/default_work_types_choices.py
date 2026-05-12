from django.db import models


class DefaultWorkTypes(models.IntegerChoices):
    EPIC = 1, "Эпик"
    STORY = 2, "История"
    WORK = 3, "Задача"
    PROBLEM = 4, "Проблема"

    @property
    def slug(self) -> str:
        return self.name.lower()

    @property
    def description(self) -> str:
        return {
            'EPIC': 'Тип работы для обозначения эпика',
            'STORY': 'Тип работы для обозначения пользовательской истории',
            'WORK': 'Задание для выполнения',
            'PROBLEM': 'Проблема для выполнения',
        }.get(self.name, '')

    @property
    def color(self) -> str:
        return {
            'EPIC': '#2A0BFF',
            'STORY': '#FBFF2F',
            'WORK': '#60FF58',
            'PROBLEM': '#ff0f0f',
        }.get(self.name, '')
