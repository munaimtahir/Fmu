from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from sims_backend.common_permissions import IsAdminOrRegistrarReadOnlyFacultyStudent
from .models import Enrollment
from .serializers import EnrollmentSerializer

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated, IsAdminOrRegistrarReadOnlyFacultyStudent]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["student__reg_no", "section__course__code", "status"]
    ordering_fields = ["id", "status"]
