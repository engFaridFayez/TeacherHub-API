from django.shortcuts import get_object_or_404, render
from rest_framework.generics import ListAPIView
from rest_framework import permissions
from rest_framework.views import APIView, Response
from core.models import Choice, Course, VideoAccess, ExamAttempt, Homework, HomeworkSubmission, Question, Stage, StudentAnswer, Term, Video,Exam
from core.serializers import CourseSerializer, ExamSerializer, StageSerializer, StudentHomeworkSerializer, TermSerializer, VideoSerializer
from rest_framework import status
from django.utils import timezone
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
        
        has_access = VideoAccess.objects.filter(
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
        
        # يعني مينفعش الطلب يسلم اكتر من فايل للواحب الواحد هو فايل واحد فقط
        if HomeworkSubmission.objects.filter(
            student=student,
            homework=homework
        ).exists():
            return Response(
                {"error": "You already submitted this homework"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # خلاص اتأكدنا ان كل حاجه تمام ... اعمل create للواجب بقي للطالب 
        HomeworkSubmission.objects.create(
            student=student,
            homework=homework,
            file=homework_file
        )
        return Response(
            {"message": "Homework submitted successfully"},
            status=status.HTTP_201_CREATED
        )
    
class ShowStudentHomeworksubmission(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):
        student = request.user

        homeworks = HomeworkSubmission.objects.filter(student=student)
        if not homeworks.exists():
            return Response(
                {"message": "you don't have any homework submissions yet!"},
                status=400
            )
        
        serializer = StudentHomeworkSerializer(homeworks,many=True)

        return Response({
            "message":"your homeworks:",
            "data":serializer.data
        })
    

class ExamView(ListAPIView):
    queryset = Exam.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ExamSerializer
    

class SubmitAnswer(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request,exam_id):
        exam = get_object_or_404(Exam,id=exam_id)

        question_id = request.data.get("question_id")
        choice_id = request.data.get("choice_id")

        question = get_object_or_404(
            Question,
            id = question_id,
            exam=exam
        )
        choice = get_object_or_404(
            Choice,
            id = choice_id,
            question=question
        )

        attempt, created = ExamAttempt.objects.get_or_create(
            student = request.user,
            exam = exam
        ) 

        if attempt.is_submitted:
            return Response(
                {"error": "Exam already submitted"},
                status=400
            )

        StudentAnswer.objects.update_or_create(
            attempt=attempt,
            question=question,
            defaults={
                "choice": choice
            }
        )

        return Response({"message":"Answer submitted successfully!"})
    

class SubmitExam(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request,exam_id):
        attempt = get_object_or_404(
            ExamAttempt,
            student=request.user,
            exam_id=exam_id
        )

        if attempt.is_submitted:
            return Response(
                {"error": "Exam already submitted"},
                status=400
            )
        
        score = 0

        for answer in attempt.answers.all():
            if answer.choice.is_correct:
                score += answer.question.degree

        total_degree = sum(
            q.degree
            for q in Question.objects.filter(exam=attempt.exam)
        )

        percentage = (score / total_degree) * 100 if total_degree > 0 else 0

        is_passed = percentage >= attempt.exam.pass_percentage

        attempt.score = score
        attempt.percentage = percentage
        attempt.is_passed = is_passed
        attempt.is_submitted = True
        attempt.submitted_at = timezone.now()
        attempt.save()

        return Response({
            "score": score,
            "message": "Exam submitted successfully"
        })
