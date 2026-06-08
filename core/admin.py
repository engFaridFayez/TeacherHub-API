from django.contrib import admin

from core.models import *

# Register your models here.
admin.site.register(Stage)
admin.site.register(Term)
admin.site.register(Course)
admin.site.register(Video)
admin.site.register(CourseAccess)
admin.site.register(Homework)
admin.site.register(HomeworkSubmission)
admin.site.register(Exam)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Progress)