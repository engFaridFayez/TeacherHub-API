from rest_framework import serializers

from core.models import Choice, Course, Exam, ExamAttempt, Homework, HomeworkSubmission, Progress, Question, QuestionTitle, Stage, StudentAnswer, Term, Video, VideoAccess


######################################
#        READ SERIALIZERS
######################################
class StageReadSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Stage
        fields = [
            'id',
            'name',
            'description'
        ]

class TermReadSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Term
        fields = [
            'id',
            'name',
            'stage'
        ]

class CourseReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            'id',
            'name',
            'description',
            'term',
            'created_at',
        ]

class VideoReadSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Video
        fields = [
            'id',
            'course',
            'name',
            'video_type',
            'video_file',
            'iframe_url',
            'created_at'
        ]

class VideoAccessReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoAccess
        fields = [
            'id',
            'is_active',
            'max_views',
            'views_used'
        ]


class HomeworkReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = [
            'id',
            'course',
            'title',
            'submission_type'
        ]

class HomeworkSubmissionReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeworkSubmission
        fields = [
            'id',
            'student',
            'homework',
            'file',
            'image',
            'created_at'
        ]

class ExamReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = [
            'id',
            'course',
            'title',
            'pass_percentage'
        ]

class QuestionTitleReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionTitle
        fields = [
            'id',
            'name',
            'answer_type',
        ]

class QuestionReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = [
            'id',
            'exam',
            'title',
            'text',
            'degree',
        ]

class ChoiceReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Choice
        fields = [
            'id',
            'question',
            'text',
        ]

class ProgressReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = [
            'id',
            'student',
            'course',
            'videos_watched',
            'exam_passed',
            'homework_done',
        ]
class ExamAttemptReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamAttempt
        fields = [
            'id',
            'exam',
            'started_at',
            'submitted_at',
            'score',
            'is_submitted',
            'percentage',
            'is_passed',
        ]

class StudentAnswerReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAnswer
        fields = [
            'id',
            'attempt',
            'question',
            'choice',
            'text_answer',
            'answered_at',
        ]



######################################
#        WRITE SERIALIZERS
######################################
class StageWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stage
        fields = [
            'name',
            'description',
        ]



class TermWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Term
        fields = [
            'name',
            'stage',
        ]


class CourseWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = [
            'name',
            'description',
            'term',
        ]


class VideoWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Video
        fields = [
            'course',
            'name',
            'video_type',
            'video_file',
            'iframe_url',
        ]


class VideoAccessWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = VideoAccess
        fields = [
            'student',
            'video',
            'is_active',
            'max_views',
        ]

class HomeworkWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Homework
        fields = [
            'course',
            'title',
            'submission_type',
        ]

class HomeworkSubmissionWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = HomeworkSubmission
        fields = [
            'homework',
            'file',
            'image',
        ]

class ExamWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Exam
        fields = [
            'course',
            'title',
            'pass_percentage',
        ]

class QuestionTitleWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionTitle
        fields = [
            'name',
            'answer_type',
        ]

class QuestionWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = [
            'exam',
            'title',
            'text',
            'degree',
        ]

class ChoiceWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Choice
        fields = [
            'question',
            'text',
            'is_correct',
        ]