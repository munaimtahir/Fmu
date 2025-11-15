"""Custom views for authentication and dashboard."""
import logging

from django.db.models import Count, ExpressionWrapper, F, FloatField, Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from sims_backend.academics.models import Course, Section
from sims_backend.admissions.models import Student
from sims_backend.attendance.models import Attendance
from sims_backend.common_permissions import in_group
from sims_backend.enrollment.models import Enrollment
from sims_backend.requests.models import Request
from sims_backend.results.models import Result

from .serializers import EmailTokenObtainPairSerializer

logger = logging.getLogger(__name__)


class EmailTokenObtainPairView(TokenObtainPairView):
    """
    Custom token view that accepts email instead of username.

    This view uses the EmailTokenObtainPairSerializer to allow
    users to authenticate using their email address.
    """

    serializer_class = EmailTokenObtainPairSerializer  # type: ignore[assignment]


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """
    Get dashboard statistics based on user role
    """
    user = request.user

    stats = {}

    # Common stats
    if user.is_superuser or in_group(user, "Admin") or in_group(user, "Registrar"):
        # Admin/Registrar sees all statistics
        stats = {
            "total_students": Student.objects.filter(status="active").count(),
            "total_courses": Course.objects.count(),
            "active_sections": Section.objects.count(),
            "pending_requests": Request.objects.filter(status="pending").count(),
            "published_results": Result.objects.filter(state="published").count(),
            "ineligible_students": _count_ineligible_students(),
        }
    elif in_group(user, "Faculty"):
        # Faculty sees only their own sections and students
        faculty_sections = Section.objects.filter(teacher=user)
        enrolled_students = Enrollment.objects.filter(
            section__in=faculty_sections
        ).values_list('student', flat=True).distinct()

        stats = {
            "my_sections": faculty_sections.count(),
            "my_students": enrolled_students.count(),
            "pending_attendance": _count_pending_attendance(faculty_sections),
            "draft_results": Result.objects.filter(
                section__in=faculty_sections,
                state="draft"
            ).count(),
        }
    elif in_group(user, "Student"):
        # Student sees their own stats
        # Try to find student by name (temporary solution)
        # TODO: Add proper User to Student relationship via ForeignKey
        try:
            student = Student.objects.get(name=f"{user.first_name} {user.last_name}")
            my_enrollments = Enrollment.objects.filter(student=student)

            stats = {
                "enrolled_courses": my_enrollments.count(),
                "attendance_rate": _calculate_attendance_rate(student),
                "completed_results": Result.objects.filter(
                    student=student,
                    state="published"
                ).count(),
                "pending_requests": Request.objects.filter(
                    student=student,
                    status="pending"
                ).count(),
            }
        except Student.DoesNotExist:
            logger.warning(f"No student record found for user {user.username}")
            stats = {
                "error": "No student record found for this user"
            }
    else:
        stats = {
            "message": "No statistics available for your role"
        }

    return Response(stats, status=status.HTTP_200_OK)


def _count_ineligible_students():
    """
    Count students who are ineligible due to low attendance
    Ineligible = attendance < 75%
    """
    active_students = (
        Student.objects.filter(status="active")
        .annotate(
            total_attendance=Count("attendance"),
            present_attendance=Count(
                "attendance",
                filter=Q(attendance__present=True),
            ),
        )
        .filter(total_attendance__gt=0)
        .annotate(
            attendance_rate=ExpressionWrapper(
                (F("present_attendance") * 100.0) / F("total_attendance"),
                output_field=FloatField(),
            ),
        )
    )

    return active_students.filter(attendance_rate__lt=75).count()

def _count_pending_attendance(sections):
    """
    Count sections that need attendance marking (basic heuristic)
    """
    from datetime import date, timedelta

    # Count sections with no attendance in last 7 days
    last_week = date.today() - timedelta(days=7)
    if not hasattr(sections, "annotate"):
        section_ids = [section.pk for section in sections]
        sections = Section.objects.filter(pk__in=section_ids)
    return (
        sections.annotate(
            recent_attendance=Count(
                "attendance",
                filter=Q(attendance__date__gte=last_week),
            )
        )
        .filter(recent_attendance=0)
        .count()
    )


def _calculate_attendance_rate(student):
    """
    Calculate attendance rate for a student
    """
    total = Attendance.objects.filter(student=student).count()
    if total == 0:
        return 0.0

    present = Attendance.objects.filter(student=student, present=True).count()
    return round((present / total) * 100, 2)
