from django.urls import path
from . import views

urlpatterns = [
    path('create/course/', views.CourseCreateView.as_view()),
    path('update/course/<int:pk>/', views.CourseDetailView.as_view()),
    path('create/materials/', views.CourseMaterialCreateView.as_view()),
    path('update/materials/<int:pk>/', views.UpdateDeleteCourseMaterialView.as_view()),
    path('enroll/course/', views.EnrollCourseView.as_view()),
    path('unenroll/course/', views.UnenrollCourseView.as_view())
]