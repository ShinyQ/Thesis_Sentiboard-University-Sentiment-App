from django.urls import path
from . import views

app_name = 'sentiment'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('manage', views.manage, name='manage'),
    path('crawl', views.crawl, name='crawl'),
    path('crawl_save', views.crawl_save, name='crawl_save'),
    path('crawl_tweets', views.crawl_tweets, name='crawl_tweets'),
    path('delete_sentiment', views.delete_sentiment, name='delete_sentiment'),
]