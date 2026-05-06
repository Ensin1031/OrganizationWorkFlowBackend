from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated

from permissions.api.mixins import ACLViewSetMixin
from work.api.filters import WorkFilter
from work.api.serializers import WorkSerializer
from work.models.work import Work


class WorkViewSet(ACLViewSetMixin):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'

    filterset_class = WorkFilter

    search_fields = ['name', 'slug']

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_active=True).order_by('-slug', '-updated')
        return queryset

    def create(self, request, *args, **kwargs):
        if not request.data.get('created_by_id'):
            try:
                request.data._mutable = True
            except AttributeError:
                pass
            request.data['created_by_id'] = request.user.id
        return super().create(request, *args, **kwargs)
