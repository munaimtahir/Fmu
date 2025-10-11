from django.db import models
from sims_backend.admissions.models import Student
from sims_backend.academics.models import Section

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'section')

    def __str__(self):
        return f"{self.student} enrolled in {self.section}"