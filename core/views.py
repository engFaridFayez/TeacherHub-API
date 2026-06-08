from django.shortcuts import get_object_or_404, render
from rest_framework.generics import ListAPIView
from rest_framework import permissions
from rest_framework.views import APIView, Response
from core.models import Course, CourseAccess, Homework, HomeworkSubmission, Stage, Term, Video
from core.serializers import CourseSerializer, StageSerializer, TermSerializer, VideoSerializer
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
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
    

class CoursesList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, term_id):
        courses = Course.objects.filter(term_id=term_id)

        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

class CourseDetails(APIView):
    permission_classes = [permissions.IsAuthenticated]
    

    def get(self,request,course_id,term_id):
        user = request.user
        course = get_object_or_404(Course,
                                    id=course_id,
                                    term_id=term_id)
        
        has_access = CourseAccess.objects.filter(
            student = user,
            course = course,
            is_active = True
        ).exists()

        if not has_access:
            return Response(
                {"detail": "انت لسه مدفعتش فلوس الحصة"},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer= CourseSerializer(course)
        return Response(serializer.data)

class VideosList(ListAPIView):
    serializer_class = VideoSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        course= self.kwargs['course_id']
        return Video.objects.filter(course_id=course)

class StudentSubmitHomework(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    def post(self,request):
        student = request.user
        homework_id = request.data.get("homework_id")
        homework_file = request.FILES.get("homework_file")

        if not homework_id:
            return Response({"message","Homework Id is required"},
                            status=status.HTTP_400_BAD_REQUEST)
        if not homework_file:
            return Response(
                {"error": "Homework file is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            homework = Homework.objects.get(id=homework_id)
        except Homework.DoesNotExist:
            return Response(
                {"error": "Homework not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        if HomeworkSubmission.objects.filter(
            student=student,
            homework=homework
        ).exists():
            return Response(
                {"error": "You already submitted this homework"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        HomeworkSubmission.objects.create(
            student=student,
            homework=homework,
            file=homework_file
        )
        return Response(
            {"message": "Homework submitted successfully"},
            status=status.HTTP_201_CREATED
        )