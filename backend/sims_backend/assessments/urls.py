from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AssessmentViewSet, AssessmentScoreViewSet

router = DefaultRouter()
router.register(r'assessments', AssessmentViewSet)
router.register(r'assessment-scores', AssessmentScoreViewSet)

urlpatterns = [
    path('', include(router.urls)),
]