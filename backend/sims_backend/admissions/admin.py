
    from django.contrib import admin
    from .models import Student

    @admin.register(Student)
    class StudentAdmin(admin.ModelAdmin):
        list_display = ("reg_no", "name", "program", "status")
        search_fields = ("reg_no", "name", "program", "status")
        list_filter = ("program", "status")
        ordering = ("reg_no",)
    
