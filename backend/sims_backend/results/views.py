from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from sims_backend.common_permissions import IsAdminOrRegistrarReadOnlyFacultyStudent
from .models import Result
from .serializers import ResultSerializer

class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    permission_classes = [IsAuthenticated, IsAdminOrRegistrarReadOnlyFacultyStudent]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["student__reg_no", "section__course__code", "final_grade"]
    ordering_fields = ["id", "published_at"]
