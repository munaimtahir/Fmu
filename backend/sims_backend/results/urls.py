from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ResultViewSet

router = DefaultRouter()
router.register(r'results', ResultViewSet)

urlpatterns = [
    path('', include(router.urls)),
]