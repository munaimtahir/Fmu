
    from django.db import models

    class Student(models.Model):
        reg_no = models.CharField(max_length=32, unique=True)
        name = models.CharField(max_length=255)
        program = models.CharField(max_length=128)
        status = models.CharField(max_length=32)

        class Meta:
            ordering = ["reg_no"]

        def __str__(self) -> str:
            return f"{self.reg_no} - {self.name}"
    
