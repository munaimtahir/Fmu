from django.db import models
from sims_backend.admissions.models import Student
from sims_backend.academics.models import Section

class Assessment(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='assessments')
    name = models.CharField(max_length=100)
    max_score = models.IntegerField()

    def __str__(self):
        return f"{self.name} for {self.section}"

class AssessmentScore(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='scores')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='scores')
    score = models.IntegerField()

    class Meta:
        unique_together = ('assessment', 'student')

    def __str__(self):
        return f"{self.student} score for {self.assessment}: {self.score}"