from rest_framework import serializers

from .models import Course, Program, Section, Term


class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = Term
        fields = ["id", "name", "status", "start_date", "end_date"]


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = ["id", "name", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at"]


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "code", "title", "credits", "program"]


class SectionSerializer(serializers.ModelSerializer):
    # teacher_name can be written when teacher is None, 
    # but is auto-populated from teacher when teacher is set
    teacher_name = serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model = Section
        fields = ["id", "course", "term", "teacher", "teacher_name", "capacity"]
