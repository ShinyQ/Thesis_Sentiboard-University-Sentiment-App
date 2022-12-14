import logging
from django.shortcuts import render

from django.http import HttpResponse
from django_db_logger.models import StatusLog

logger = logging.getLogger('db')

def __gen_500_errors(request):
    try:
        1/0
    except Exception as e:
        logger.exception(e)

    return HttpResponse('Hello 500!')

def xdlog(request):
    context = {}
    context['logs'] = StatusLog.objects.all()
    return render(request, 'log/xdlog.html', context)