from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from sims_backend.common_permissions import IsAdminOrRegistrarReadOnlyFacultyStudent
from .models import Program, Course, Section
from .serializers import ProgramSerializer, CourseSerializer, SectionSerializer

class ProgramViewSet(viewsets.ModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = [IsAuthenticated, IsAdminOrRegistrarReadOnlyFacultyStudent]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["id", "name"]

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsAdminOrRegistrarReadOnlyFacultyStudent]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["code", "title"]
    ordering_fields = ["id", "code", "title", "credits"]

class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [IsAuthenticated, IsAdminOrRegistrarReadOnlyFacultyStudent]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["course__code", "term", "teacher"]
    ordering_fields = ["id", "term", "teacher"]
