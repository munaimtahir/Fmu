from rest_framework import serializers
from .models import Assessment, AssessmentScore
class AssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = ["id", "section", "type", "weight"]
class AssessmentScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentScore
        fields = ["id", "assessment", "student", "score", "max_score"]
