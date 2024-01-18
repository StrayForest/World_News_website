# news/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('country/<str:country_name>/', views.country_news, name='country_news'),
    path('news/<int:news_id>/', views.news_detail, name='news_detail'),
    # Другие URL-адреса вашего приложения
]
