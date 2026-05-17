from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated

from comments.api.filters import WorkCommentFilter
from comments.api.serializers import WorkCommentSerializer
from comments.models import WorkComment
from permissions.api.mixins import ACLViewSetMixin


class WorkCommentViewSet(ACLViewSetMixin):
    queryset = WorkComment.objects.all()
    serializer_class = WorkCommentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = WorkCommentFilter

    search_fields = ['description',]

    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_active=True).order_by('-updated')
        return queryset
