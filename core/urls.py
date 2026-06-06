from django.urls import path

from core import views

urlpatterns = [
    path('stages/', views.StageList.as_view(), name='stages-list'),
    path('terms/<int:stage_id>/', views.TermsList.as_view(), name='terms-list'),
    # path('terms/', views.AllTermsList.as_view(), name='terms-list'),
    path('courses/<int:term_id>/', views.CoursesList.as_view(), name='courses-list'),
    path('videos/<int:course_id>/', views.VideosList.as_view(), name='videos-list'),
]