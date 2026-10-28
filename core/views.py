from rest_framework import viewsets

from core.models import Stage, Term
from core.serializers import (
    StageReadSerializer,
    StageWriteSerializer,
    TermReadSerializer,
    TermWriteSerializer,
)

class StageViewSet(viewsets.ModelViewSet):
    queryset = Stage.objects.all()

    def get_serializer_class(self):
        if self.action in ['list','retrieve']:
            return StageReadSerializer

        return StageWriteSerializer

class TermViewSet(viewsets.ModelViewSet):
    queryset = Term.objects.prefetch_related("stage")

    def get_serializer_class(self):
        if self.action in ['list','retrieve']:
            return TermReadSerializer
        return TermWriteSerializer