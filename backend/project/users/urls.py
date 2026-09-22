from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('details/', views.UserDetailView.as_view()),
    path('create/profile/', views.CreateProfileView.as_view()),
]