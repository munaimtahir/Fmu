from django.db import models
from sims_backend.admissions.models import Student
from sims_backend.academics.models import Section

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    present = models.BooleanField(default=False)
    reason = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ('student', 'section', 'date')

    def __str__(self):
        status = "Present" if self.present else "Absent"
        return f"{self.student} in {self.section} on {self.date}: {status}"