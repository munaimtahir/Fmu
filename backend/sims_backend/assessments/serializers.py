from rest_framework import serializers
from .models import Assessment, AssessmentScore

class AssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = '__all__'

class AssessmentScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentScore
        fields = '__all__'