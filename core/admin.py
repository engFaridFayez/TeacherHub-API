from django.contrib import admin

from core.models import Course, Stage, Term, Video

# Register your models here.
admin.site.register(Stage)
admin.site.register(Term)
admin.site.register(Course)
admin.site.register(Video)