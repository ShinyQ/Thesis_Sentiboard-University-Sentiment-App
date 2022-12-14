from . import views

from django.urls import path
from django.contrib.auth import views as auth_views

app_name = 'auth'
urlpatterns = [
    path('login', auth_views.LoginView.as_view(template_name='auth/system-login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('register', views.sign_up, name="register"),
    path('register-success', views.regsuccess, name="regsuccess"),
]