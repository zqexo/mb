from django.urls import path

from users.apps import UsersConfig
from users import views

app_name = UsersConfig.name

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('email-confirm/<str:token>/', views.email_verification, name='email_confirm'),
    path('password-reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('edit-profile/', views.EditProfileView.as_view(), name='edit_profile'),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('edit-profile/avatar/', views.edit_avatar, name='edit_avatar'),
]
