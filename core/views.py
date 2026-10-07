from rest_framework import viewsets

from core.models import Stage
from core.serializers import (
    StageReadSerializer,
    StageWriteSerializer,
)

class StageViewSet(viewsets.ModelViewSet):
    queryset = Stage.objects.all()

    def get_serializer_class(self):
        if self.action in ['list','retrieve']:
            return StageReadSerializer

        return StageWriteSerializer

