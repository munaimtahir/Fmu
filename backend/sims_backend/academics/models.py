from django.db import models

class Program(models.Model):
    name = models.CharField(max_length=100, unique=True)
    department = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Course(models.Model):
    code = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='courses')

    def __str__(self):
        return f"{self.code}: {self.title}"

class Section(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sections')
    section_identifier = models.CharField(max_length=20)
    semester = models.CharField(max_length=50)
    # Assuming a User model might be used for faculty later
    # faculty = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ('course', 'section_identifier', 'semester')

    def __str__(self):
        return f"{self.course.code} - {self.section_identifier} ({self.semester})"