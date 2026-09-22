from django.urls import path
from . import views

urlpatterns = [
    path('department/', views.DepartmentListView.as_view()),
    path('programme/', views.ProgrammeListView.as_view()),
]