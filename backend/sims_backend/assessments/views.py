from rest_framework import viewsets
from .models import Assessment, AssessmentScore
from .serializers import AssessmentSerializer, AssessmentScoreSerializer

class AssessmentViewSet(viewsets.ModelViewSet):
    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer

class AssessmentScoreViewSet(viewsets.ModelViewSet):
    queryset = AssessmentScore.objects.all()
    serializer_class = AssessmentScoreSerializer