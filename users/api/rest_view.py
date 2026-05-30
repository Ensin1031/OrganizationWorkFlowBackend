from django.db.models import Q, Case, When, Value, IntegerField
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, status
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from permissions.api.mixins import ACLViewSetMixin
from project.api.serializers import ProjectShortSerializer
from project.models import Project
from sprint.api.serializers import SprintShortSerializer
from sprint.models import Sprint
from users.api.serializers import UserSerializer, CustomTokenObtainPairSerializer, GlobalSearchResponseSerializer
from users.models import UserExtended
from utils.choices.default_work_types_choices import DefaultWorkTypes
from work.api.serializers import WorkShortSerializer
from work.models.work import Work


class RegisterView(generics.CreateAPIView):
    queryset = UserExtended.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class LogoutView(APIView):
    http_method_names = ['post']
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response(
                    {"detail": "Refresh token is required."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            token = RefreshToken(refresh_token)
            token.blacklist()  # добавляем токен в черный список

            return Response(
                {"detail": "Successfully logged out."},
                status=status.HTTP_200_OK
            )
        except (TokenError, InvalidToken):
            return Response(
                {"detail": "Invalid or expired refresh token."},
                status=status.HTTP_400_BAD_REQUEST
            )


class UserExtendedViewSet(ACLViewSetMixin):
    queryset = UserExtended.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]

    search_fields = ['first_name', 'second_name', 'last_name']

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_active=True)
        return queryset


class GlobalSearchViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    DEFAULT_PAGE = 1
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGE_SIZE = 1000

    def paginate_queryset(self, queryset, serializer_class, request):
        page = int(request.query_params.get('page', self.DEFAULT_PAGE))
        page_size = min(int(request.query_params.get('page_size', self.DEFAULT_PAGE_SIZE)), self.MAX_PAGE_SIZE)

        offset = (page - 1) * page_size
        limit = offset + page_size
        total_count = queryset.count()

        return {
            'count': total_count,
            'has_next_page': total_count > page_size,
            'results': serializer_class(
                queryset[offset:limit],
                many=True,
                context={'request': request},
            ).data,
        }

    def list(self, request):
        search = request.query_params.get('search', '').strip()

        projects_qs = Project.objects.filter(is_active=True)
        sprints_qs = Sprint.objects.filter(is_active=True)
        epiks_qs = Work.objects.filter(is_active=True, type_id=DefaultWorkTypes.EPIC)
        histories_qs = Work.objects.filter(is_active=True, type_id=DefaultWorkTypes.STORY)
        tasks_qs = Work.objects.exclude(
            type_id__in=[DefaultWorkTypes.EPIC, DefaultWorkTypes.STORY],
        ).filter(
            is_active=True,
        )

        if search:
            projects_qs = projects_qs.filter(Q(name__icontains=search) | Q(code_prefix__icontains=search))
            sprints_qs = sprints_qs.filter(Q(name__icontains=search))
            epiks_qs = epiks_qs.filter(Q(name__icontains=search) | Q(slug__icontains=search))
            histories_qs = histories_qs.filter(Q(name__icontains=search) | Q(slug__icontains=search))
            tasks_qs = tasks_qs.filter(Q(name__icontains=search) | Q(slug__icontains=search))
        else:
            projects_qs = projects_qs.none()
            sprints_qs = sprints_qs.none()
            epiks_qs = epiks_qs.none()
            histories_qs = histories_qs.none()
            tasks_qs = tasks_qs.none()

        return Response(
            GlobalSearchResponseSerializer(
                {
                    'projects': self.paginate_queryset(
                        projects_qs.order_by('-updated'),
                        ProjectShortSerializer,
                        request,
                    ),
                    'sprints': self.paginate_queryset(
                        sprints_qs.annotate(
                            sort_order=Case(
                                When(in_work=True, is_completed=False, then=Value(1)),
                                When(in_work=False, is_completed=False, then=Value(2)),
                                When(in_work=True, is_completed=True, then=Value(3)),
                                default=Value(4),
                                output_field=IntegerField(),
                            )
                        ).order_by('sort_order', '-updated'),
                        SprintShortSerializer,
                        request,
                    ),
                    'epiks': self.paginate_queryset(
                        epiks_qs.order_by('-slug', '-updated'),
                        WorkShortSerializer,
                        request,
                    ),
                    'histories': self.paginate_queryset(
                        histories_qs.order_by('-slug', '-updated'),
                        WorkShortSerializer,
                        request,
                    ),
                    'tasks': self.paginate_queryset(
                        tasks_qs.order_by('-slug', '-updated'),
                        WorkShortSerializer,
                        request,
                    ),
                }
            ).data
        )
