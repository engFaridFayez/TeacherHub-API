from django.urls import path

from core import views

urlpatterns = [
    # Stages / Terms / Courses
    path('stages/', views.StageList.as_view()),
    path('terms/<int:stage_id>/', views.TermsList.as_view()),
    path('courses/<int:term_id>/', views.CoursesList.as_view()),
    path('courses/<int:term_id>/<int:course_id>/', views.CourseDetails.as_view()),

    # Videos
    path('courses/<int:course_id>/videos/', views.VideosList.as_view()),

    # Homework
    path('homework/submit/', views.StudentSubmitHomework.as_view()),
    path('myhomeworks/', views.ShowStudentHomeworksubmission.as_view()),

    # Exams
    path('exams/', views.ExamView.as_view()),
    path('exams/<int:exam_id>/answer/', views.SubmitAnswer.as_view()),
    path('exams/<int:exam_id>/submit/', views.SubmitExam.as_view()),
]