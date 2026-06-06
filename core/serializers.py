from rest_framework import serializers

from core.models import Course, Stage, Term, Video

class StageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Stage
        fields = '__all__'

class TermSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Term
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Course
        fields = '__all__'

class VideoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Video
        fields = '__all__'