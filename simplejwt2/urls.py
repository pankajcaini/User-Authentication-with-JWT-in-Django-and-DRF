
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.UserRegistrationView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('profile/', views.UserProfileView.as_view()),
    path('password_change/', views.UserChangePasswordView.as_view()),
    path('reset_password/', views.SendResetPasswordLinkView.as_view()),
    path('reset_password/<uid>/<token>/', views.ResetPasswordView.as_view()),
]
