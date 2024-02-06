from django.shortcuts import render
from .models import News, Country
from django.shortcuts import get_object_or_404

def home(request):
    countries = Country.objects.all()
    latest_news = {}

    for country in countries:
        news = get_top_news_by_country(country.name).first()
        if news:
            latest_news[country] = news

    return render(request, 'home.html', {'latest_news': latest_news})

def get_top_news_by_country(country_name):
    return News.objects.filter(country_name=country_name)

def country_news(request, country_name):
    country = get_object_or_404(Country, name=country_name)
    # Сортировка сначала по дате (новые вначале), затем по searches (убывание)
    news_list = News.objects.filter(country_name=country).exclude(content_review__isnull=True).exclude(content_review='').exclude(content_review__istartswith='Error').order_by('-date', '-searches')[:20]
    return render(request, 'country_news.html', {'news_list': news_list, 'country': country})


def news_detail(request, country_name, news_id):
    news = get_object_or_404(News, pk=news_id)
    country = get_object_or_404(Country, name=country_name)
    return render(request, 'news_detail.html', {'news': news, 'country': country})


