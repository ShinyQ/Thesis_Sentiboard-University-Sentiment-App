from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

app_name = 'django_db_logger'
urlpatterns = [
    path('log', views.xdlog, name="xdlog"),
]