from rest_framework import serializers

from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["id", "reg_no", "name", "program", "status"]
        read_only_fields = ["id"]

    def validate_reg_no(self, value: str) -> str:
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Registration number is required.")
        return value
