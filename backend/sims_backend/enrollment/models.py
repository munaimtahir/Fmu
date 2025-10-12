from django.db import models


class Enrollment(models.Model):
    student = models.ForeignKey(
        "admissions.Student", on_delete=models.CASCADE, related_name="enrollments"
    )
    section = models.ForeignKey(
        "academics.Section", on_delete=models.CASCADE, related_name="enrollments"
    )
    status = models.CharField(max_length=32, default="enrolled")

    class Meta:
        unique_together = ("student", "section")
