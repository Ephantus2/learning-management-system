from django.urls import path
from . import views

urlpatterns = [
    path('create/assessment/', views.AssessmentCreateView.as_view()),
    path('update/assessment/<int:pk>/', views.updateDeleteAssessmentView.as_view()),
    path('course/assessments/<str:course_code>/', views.courseAssessmentsView.as_view()),
    path('create/submission/', views.SubmissionCreateView.as_view()),
    path('update/submission/<int:pk>/', views.updateDeleteSubmissionView.as_view()),
    path('create/grade/', views.GradeCreateView.as_view()),
    path('update/grade/<int:pk>/', views.GradeUpdateView.as_view),
    path('view/grade/<int:pk>/', views.ViewGradeView.as_view()),
    path('submissions/<int:pk>/',views.submissionsView.as_view()),
    path('mysubmissions/', views.MySubmissionsView.as_view()),
]