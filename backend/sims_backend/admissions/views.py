from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated

from .models import Student
from .permissions import IsAdminOrRegistrarOrReadOwnStudent, _in_group
from .serializers import StudentSerializer


class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, IsAdminOrRegistrarOrReadOwnStudent]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["reg_no", "name", "program", "status"]
    ordering_fields = ["id", "reg_no", "name", "program", "status"]
    queryset = Student.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if _in_group(user, "Student") and not (
            user.is_superuser
            or _in_group(user, "Admin")
            or _in_group(user, "Registrar")
        ):
            return qs.filter(reg_no=getattr(user, "username", ""))
        return qs
