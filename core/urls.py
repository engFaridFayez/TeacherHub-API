from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import StageViewSet

router = DefaultRouter()

router.register('stages', StageViewSet,basename='stage')

urlpatterns = router.urls