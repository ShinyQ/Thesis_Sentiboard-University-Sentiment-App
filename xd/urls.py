"""xd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import django_db_logger.views
from django.shortcuts import redirect
import datetime
import logging
import json
from django.http import JsonResponse
import os
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)

@csrf_exempt
def pull(request) :

    # gihub webhook harus POST
    if request.method == "POST" :
        # running git pull
        stream = os.popen('pwd')
        output_pwd = stream.read()

        stream = os.popen('git pull')
        output_pull = stream.read()

        message = str(datetime.datetime.now())+' | pwd : '+ output_pwd +' |  git pull from POST : ' + output_pull

        response_data = {}
        response_data['code'] = '200'
        response_data['message'] = message

        logger.error(message)

        return JsonResponse(response_data)
    else :
                # running git pull
        stream = os.popen('pwd')
        output_pwd = stream.read()

        stream = os.popen('git pull')
        output_pull = stream.read()

        message = str(datetime.datetime.now())+' | pwd : '+ output_pwd +' |  git pull from GET: ' + output_pull

        response_data = {}
        response_data['code'] = '200'
        response_data['message'] = message

        logger.error(message)

        return JsonResponse(response_data)

urlpatterns = [
    path('', lambda request: redirect('sentiment/dashboard', permanent = True)),
    path('sentiment/', include('sentiment.urls')),
    path('auth/', include('auth.urls')),
    path('django_db_logger/', include('django_db_logger.urls')),
    path('log', django_db_logger.views.xdlog, name="xdlog"),
]


