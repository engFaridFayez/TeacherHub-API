from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework import permissions
from core.models import Course, Stage, Term, Video
from core.serializers import CourseSerializer, StageSerializer, TermSerializer, VideoSerializer

# Create your views here.
class StageList(ListAPIView):
    queryset = Stage.objects.all()
    serializer_class = StageSerializer
    permission_classes = [permissions.AllowAny]

# class AllTermsList(ListAPIView):
#     queryset = Term.objects.all()
#     serializer_class = TermSerializer
#     permission_classes = [permissions.AllowAny]


class TermsList(ListAPIView):
    serializer_class = TermSerializer
    permission_classes = [permissions.AllowAny]
    def get_queryset(self):
        
        stage = self.kwargs['stage_id']
        return Term.objects.filter(stage__id=stage)
    

class CoursesList(ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        term = self.kwargs['term_id']
        return Course.objects.filter(term__id=term)
    
class VideosList(ListAPIView):
    serializer_class = VideoSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        course= self.kwargs['course_id']
        return Video.objects.filter(course_id=course)