from typing import Union

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from permissions.models import ACLModelMixin


class ACLViewSetMixin(ModelViewSet):

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        model: Union[ACLModelMixin] = queryset.model
        user = self.request.user
        # т.к. на данный момент права сделаны на основе Django permissions - проверяем только на доступ к записям модели
        if not user.is_authenticated or (not user.is_superuser and not user.has_perm(model._permission_name("view"))):
            return queryset.none()
        return queryset

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        model: Union[ACLModelMixin] = self.get_model_class()
        user = self.request.user
        # т.к. на данный момент права сделаны на основе Django permissions - проверяем только на доступ к записям модели
        if not user.is_authenticated or (not user.is_superuser and not user.has_perm(model._permission_name("view"))):
            return queryset.none()
        return queryset

    def get_model_class(self):
        return self.get_queryset().model

    def check_can_create(self):
        model = self.get_model_class()
        if not model.can_create(self.request.user):
            raise PermissionDenied("Недостаточно прав для создания.")

    def check_can_view(self, obj):
        if not obj.can_view(self.request.user):
            raise PermissionDenied("Недостаточно прав для просмотра.")

    def check_can_edit(self, obj):
        if not obj.can_edit(self.request.user):
            raise PermissionDenied("Недостаточно прав для изменения.")

    def check_can_delete(self, obj):
        if not obj.can_delete(self.request.user):
            raise PermissionDenied("Недостаточно прав для удаления.")

    def create(self, request, *args, **kwargs):
        self.check_can_create()
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        self.check_can_view(obj)
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        self.check_can_edit(obj)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        obj = self.get_object()
        self.check_can_edit(obj)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        self.check_can_delete(obj)
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=["GET", ], url_path="can-create", url_name="can-create")
    def can_create(self, request, *args, **kwargs) -> Response:
        return Response(
            data={'can_create': self.get_model_class().can_create(user=self.request.user)},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["GET"], url_path="can-edit", url_name="can-edit")
    def can_edit(self, request, *args, **kwargs) -> Response:
        return Response(
            data={'can_edit': self.get_object().can_edit(user=self.request.user)},
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["GET"], url_path="can-view", url_name="can-view")
    def can_view(self, request, *args, **kwargs) -> Response:
        return Response(
            data={'can_view': self.get_object().can_view(user=self.request.user)},
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["GET"], url_path="can-delete", url_name="can-delete")
    def can_delete(self, request, *args, **kwargs) -> Response:
        return Response(
            data={'can_delete': self.get_object().can_delete(user=self.request.user)},
            status=status.HTTP_200_OK,
        )
