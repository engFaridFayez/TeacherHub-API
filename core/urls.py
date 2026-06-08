from django.urls import path

from core import views

urlpatterns = [
    path('stages/', views.StageList.as_view(), name='stages-list'),
    path('terms/<int:stage_id>/', views.TermsList.as_view(), name='terms-list'),
    # path('terms/', views.AllTermsList.as_view(), name='terms-list'),
    path('courses/<int:term_id>/', views.CoursesList.as_view(), name='courses-list'),
    path('coursedetails/<int:term_id>/<int:course_id>/', views.CourseDetails.as_view(), name='course-details'),
    path('videos/<int:course_id>/', views.VideosList.as_view(), name='videos-list'),
    path('homework/submit/',views.StudentSubmitHomework.as_view(),name="submit-homework"),
]