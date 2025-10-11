from django.db import models
from django.conf import settings
from sims_backend.admissions.models import Student
from sims_backend.academics.models import Section

class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='results')
    final_grade = models.CharField(max_length=5)
    published_at = models.DateTimeField(null=True, blank=True)
    published_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='published_results')

    class Meta:
        unique_together = ('student', 'section')

    def __str__(self):
        return f"Result for {self.student} in {self.section}: {self.final_grade}"