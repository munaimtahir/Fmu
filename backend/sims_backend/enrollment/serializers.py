from rest_framework import serializers

from .models import Enrollment


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ["id", "student", "section", "status"]

    def validate(self, data):
        """Validate enrollment capacity"""
        section = data.get("section")
        if section and self.instance is None:  # Only for new enrollments
            current_count = Enrollment.objects.filter(
                section=section, status="enrolled"
            ).count()
            if current_count >= section.capacity:
                raise serializers.ValidationError(
                    {"section": f"Section is at full capacity ({section.capacity})"}
                )
        return data
