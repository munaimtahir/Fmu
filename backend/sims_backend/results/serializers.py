from rest_framework import serializers
from .models import Result
class ResultSerializer(serializers.ModelSerializer):
    class Meta: model = Result; fields = ["id", "student", "section", "final_grade", "published_at", "published_by"]
