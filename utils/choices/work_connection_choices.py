from django.db import models


class WorkConnectionType(models.TextChoices):
    IS_BLOCKED_BY = "is_blocked_by", "Заблокирован задачей"
    BLOCKS = "blocks", "Блокирует задачу"
    CLONES = "clones", "Клон задачи"
    IS_CLONED_BY = "is_cloned_by", "Клонирован от задачи"
    DUPLICATES = "duplicates", "Дублирует задачу"
    IS_DUPLICATED_BY = "is_duplicated_by", "Дублирован от задачи"
    HAS_TO_BE_FINISHED_TOGETHER_WITH = "has_to_be_finished_together_with", "Завершить вместе с задачей"
    HAS_TO_BE_DONE_BEFORE = "has_to_be_done_before", "Нужно сделать до выполнения задачи"
    HAS_TO_BE_DONE_AFTER = "has_to_be_done_after", "Нужно сделать после выполнения задачи"
    HAS_TO_BE_STARTED_TOGETHER_WITH = "has_to_be_started_together_with", "Начать вместе с задачей"
    RELATES_TO = "relates_to", "Связана с задачей"
    IS_PARENT_TASK_OF = "is_parent_task_of", "Является родительской для задачи"
    IS_SUBTASK_OF = "is_subtask_of", "Является дочерней от задачи"
    CAUSES = "causes", "Является причиной для задачи"
    IS_CAUSED_BY = "is_caused_by", "Вызвана от задачи"


REVERSE_TYPES = {
    WorkConnectionType.IS_BLOCKED_BY: WorkConnectionType.BLOCKS,
    WorkConnectionType.BLOCKS: WorkConnectionType.IS_BLOCKED_BY,

    WorkConnectionType.CLONES: WorkConnectionType.IS_CLONED_BY,
    WorkConnectionType.IS_CLONED_BY: WorkConnectionType.CLONES,

    WorkConnectionType.DUPLICATES: WorkConnectionType.IS_DUPLICATED_BY,
    WorkConnectionType.IS_DUPLICATED_BY: WorkConnectionType.DUPLICATES,

    WorkConnectionType.HAS_TO_BE_FINISHED_TOGETHER_WITH: WorkConnectionType.HAS_TO_BE_FINISHED_TOGETHER_WITH,
    WorkConnectionType.HAS_TO_BE_STARTED_TOGETHER_WITH: WorkConnectionType.HAS_TO_BE_STARTED_TOGETHER_WITH,
    WorkConnectionType.RELATES_TO: WorkConnectionType.RELATES_TO,

    WorkConnectionType.HAS_TO_BE_DONE_BEFORE: WorkConnectionType.HAS_TO_BE_DONE_AFTER,
    WorkConnectionType.HAS_TO_BE_DONE_AFTER: WorkConnectionType.HAS_TO_BE_DONE_BEFORE,

    WorkConnectionType.IS_PARENT_TASK_OF: WorkConnectionType.IS_SUBTASK_OF,
    WorkConnectionType.IS_SUBTASK_OF: WorkConnectionType.IS_PARENT_TASK_OF,

    WorkConnectionType.CAUSES: WorkConnectionType.IS_CAUSED_BY,
    WorkConnectionType.IS_CAUSED_BY: WorkConnectionType.CAUSES,
}
