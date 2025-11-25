from django_filters.rest_framework import CharFilter, DjangoFilterBackend, FilterSet
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated

from sims_backend.common_permissions import (
    IsAdminOrRegistrarReadOnlyFacultyStudent,
    in_group,
)

from .models import Course, Program, Section, Term
from .serializers import (
    CourseSerializer,
    ProgramSerializer,
    SectionSerializer,
    TermSerializer,
)


class TermViewSet(viewsets.ModelViewSet):
    queryset = Term.objects.all().order_by("id")
    serializer_class = TermSerializer
    permission_classes = [IsAuthenticated, IsAdminOrRegistrarReadOnlyFacultyStudent]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["status"]
    search_fields = ["name"]
    ordering_fields = ["id", "name", "start_date", "end_date"]
    ordering = ["id"]


class ProgramViewSet(viewsets.ModelViewSet):
    queryset = Program.objects.all().order_by("id")
    serializer_class = ProgramSerializer
    permission_classes = [IsAuthenticated, IsAdminOrRegistrarReadOnlyFacultyStudent]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["name"]
    search_fields = ["name"]
    ordering_fields = ["id", "name"]
    ordering = ["id"]


class CourseFilter(FilterSet):
    program = CharFilter(field_name="program__name", lookup_expr="iexact")

    class Meta:
        model = Course
        fields = ["program", "credits"]


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by("id")
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsAdminOrRegistrarReadOnlyFacultyStudent]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CourseFilter
    search_fields = ["code", "title"]
    ordering_fields = ["id", "code", "title", "credits"]
    ordering = ["id"]


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all().order_by("id")
    serializer_class = SectionSerializer
    permission_classes = [IsAuthenticated, IsAdminOrRegistrarReadOnlyFacultyStudent]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["term", "course"]
    search_fields = [
        "course__code",
        "term",
        "teacher__username",
        "teacher__first_name",
        "teacher__last_name",
        "teacher_name",
    ]
    ordering_fields = ["id", "term", "teacher_name"]
    ordering = ["id"]

    def get_queryset(self):
        """Filter sections based on user role"""
        queryset = super().get_queryset()
        user = self.request.user

        # Faculty users should only see their own sections
        if (
            not user.is_superuser
            and not in_group(user, "Admin")
            and not in_group(user, "Registrar")
        ):
            if in_group(user, "Faculty"):
                queryset = queryset.filter(teacher=user)

        return queryset
