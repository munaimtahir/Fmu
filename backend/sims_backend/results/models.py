from django.db import models

class Result(models.Model):
    student = models.ForeignKey("admissions.Student", on_delete=models.CASCADE, related_name="results")
    section = models.ForeignKey("academics.Section", on_delete=models.CASCADE, related_name="results")
    final_grade = models.CharField(max_length=8, blank=True, default="")
    published_at = models.DateTimeField(null=True, blank=True)
    published_by = models.CharField(max_length=128, blank=True, default="")
