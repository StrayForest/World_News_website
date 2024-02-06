# news/urls.py

from django.urls import path
from . import views
from .views import country_news

urlpatterns = [
    path('', views.home, name='home'),
    path('country/<str:country_name>/', country_news, name='country_news'),
    path('country/<str:country_name>/news/<int:news_id>/', views.news_detail, name='news_detail'),
    # Другие URL-адреса вашего приложения
]
