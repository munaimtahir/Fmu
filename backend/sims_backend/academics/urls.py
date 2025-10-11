from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProgramViewSet, CourseViewSet, SectionViewSet

router = DefaultRouter()
router.register(r'programs', ProgramViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'sections', SectionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]