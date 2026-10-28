from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import StageViewSet, TermViewSet

router = DefaultRouter()

router.register('stages', StageViewSet,basename='stage')
router.register('terms', TermViewSet,basename='stage')

urlpatterns = router.urls