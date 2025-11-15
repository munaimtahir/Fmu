from django.conf import settings
from django.db import IntegrityError, models

from core.models import TimeStampedModel


class Term(models.Model):
    """Academic term/semester with enrollment status"""

    name = models.CharField(max_length=32, unique=True)
    status = models.CharField(
        max_length=16,
        choices=[("open", "Open"), ("closed", "Closed")],
        default="open",
    )
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.name} ({self.status})"


class Program(TimeStampedModel):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    code = models.CharField(max_length=32, unique=True)
    title = models.CharField(max_length=255)
    credits = models.PositiveSmallIntegerField(default=3)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name="courses")

    def __str__(self):
        return f"{self.code} - {self.title}"


class Section(models.Model):
    def __init__(self, *args, **kwargs):
        manual_teacher_name = None
        teacher_value = kwargs.pop("teacher", models.DEFERRED)
        if isinstance(teacher_value, str):
            manual_teacher_name = teacher_value.strip()
            teacher_value = None

        super().__init__(*args, **kwargs)

        if manual_teacher_name:
            self.teacher_name = manual_teacher_name

        if teacher_value is not models.DEFERRED:
            self.teacher = teacher_value

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="sections")
    term = models.CharField(max_length=32)
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="sections",
        null=True,
        blank=True,
        help_text="Faculty user assigned to teach this section"
    )
    teacher_name = models.CharField(
        max_length=128,
        blank=True,
        help_text="Display name for teacher (auto-populated from user)"
    )
    capacity = models.PositiveIntegerField(default=30)

    class Meta:
        unique_together = ("course", "term", "teacher")

    def save(self, *args, **kwargs):
        # Auto-populate teacher_name from teacher user when teacher is set
        # If teacher is None, keep the existing teacher_name value
        if self.teacher:
            self.teacher_name = f"{self.teacher.first_name} {self.teacher.last_name}".strip() or self.teacher.username
        elif self.teacher_name:
            duplicate_qs = Section.objects.filter(
                course=self.course,
                term=self.term,
                teacher__isnull=True,
                teacher_name=self.teacher_name,
            )
            if self.pk:
                duplicate_qs = duplicate_qs.exclude(pk=self.pk)
            if duplicate_qs.exists():
                raise IntegrityError("Section with this course, term and teacher already exists")
        super().save(*args, **kwargs)

    def __str__(self):
        teacher_display = self.teacher_name or (self.teacher.username if self.teacher else "No teacher")
        return f"{self.course.code} {self.term} ({teacher_display})"
