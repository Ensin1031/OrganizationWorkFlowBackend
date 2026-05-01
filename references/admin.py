from django.contrib import admin

from references.models.status import StatusRow
from references.models.work_difficulty import WorkDifficulty
from references.models.work_priority import WorkPriority
from references.models.work_tag import WorkTag
from references.models.work_technology import WorkTechnology
from references.models.work_type import WorkType
from utils.model_admin_mixins import ReferencesAdminMixin


@admin.register(WorkTag)
class WorkTagAdmin(ReferencesAdminMixin):
    pass


@admin.register(StatusRow)
class StatusRowAdmin(ReferencesAdminMixin):
    pass


@admin.register(WorkTechnology)
class WorkTechnologyAdmin(ReferencesAdminMixin):
    pass


@admin.register(WorkDifficulty)
class WorkDifficultyAdmin(ReferencesAdminMixin):
    pass


@admin.register(WorkPriority)
class WorkPriorityAdmin(ReferencesAdminMixin):
    pass


@admin.register(WorkType)
class WorkTypeAdmin(ReferencesAdminMixin):
    pass
