from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


class ACLViewSetMixin(ModelViewSet):

    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["GET", ], url_path="can-create", url_name="can-create")
    def can_create(self, request) -> Response:
        return Response(
            {
                'can_create': self.get_serializer().Meta.model.can_create(
                    user_id=getattr(self.request.user, 'id', None),
                    is_superuser=request.user.is_superuser
                ),
            }
        )

    @action(detail=True, methods=["GET"], url_path="can-edit", url_name="can-edit")
    def can_edit(self, request, pk=None) -> Response:
        return Response(
            {
                'can_edit': self.get_object().can_edit(
                    user_id=getattr(self.request.user, 'id', None),
                    is_superuser=request.user.is_superuser
                )
            }
        )

    @action(detail=True, methods=["GET"], url_path="can-view", url_name="can-view")
    def can_view(self, request, pk=None) -> Response:
        return Response(
            {
                'can_view': self.get_object().can_view(
                    user_id=getattr(self.request.user, 'id', None),
                    is_superuser=request.user.is_superuser
                )
            }
        )
