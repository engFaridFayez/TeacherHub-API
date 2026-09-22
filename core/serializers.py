from rest_framework import serializers

from core.models import Choice, Course, Exam, Homework, HomeworkSubmission, Question, Stage, StudentAnswer, Term, Video

class StageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Stage
        fields = '__all__'

class TermSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Term
        fields = '__all__'


class VideoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Video
        fields = '__all__'


class HomeworkSerializer(serializers.ModelSerializer):
    course = serializers.CharField(source="course.name")

    class Meta:
        model = Homework
        fields = [
            'id',
            'title',
            'file',
            'course'
        ]

class StudentHomeworkSerializer(serializers.ModelSerializer):

    class Meta:
        model = HomeworkSubmission
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    homeworks = HomeworkSerializer(many=True, read_only=True)
    class Meta:
        model = Course
        fields = [
            'id',
            'name',
            'description',
            'term',
            'created_at',
            'homeworks'
        ]



class ChoicesSerialzier(serializers.ModelSerializer):
    
    class Meta:
        model = Choice
        fields = [
            'text',
        ]

class QuestionsSerializer(serializers.ModelSerializer):
    choices = ChoicesSerialzier(source='choice_set',many=True,read_only=True)
    class Meta:
        model = Question
        fields = [
            'title',
            'text',
            'choices',
        ]

class ExamSerializer(serializers.ModelSerializer):
    questions = QuestionsSerializer(source='question_set',many=True,read_only=True)
    
    class Meta:
        model = Exam
        fields = [
            'id',
            'course',
            'title',
            'pass_percentage',
            'questions',
        ]


class AnswersSerialzier(serializers.ModelSerializer):

    class Meta:
        model = StudentAnswer
        fields = '__all__'