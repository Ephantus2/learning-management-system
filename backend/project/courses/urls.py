from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.CourseCreateView.as_view()),
    path('create/materials/', views.CourseMaterialCreateView.as_view()),
    path('enroll/', views.EnrollCourseView.as_view()),
    path('unenroll/', views.UnenrollCourseView.as_view())
]