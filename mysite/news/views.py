from django.shortcuts import render
from .models import News, Country
from django.shortcuts import get_object_or_404

def home(request):
    countries = Country.objects.all()
    latest_news = {}
    for country in countries:
        news = News.objects.filter(country=country).order_by('-published_date').first()
        if news:
            latest_news[country] = news

    return render(request, 'home.html', {'latest_news': latest_news})


def country_news(request, country_name):
    country = get_object_or_404(Country, name=country_name)
    news = News.objects.filter(country=country)
    return render(request, 'country_news.html', {'country': country, 'news': news})


def news_detail(request, news_id):
    news_item = get_object_or_404(News, id=news_id)
    return render(request, 'news_detail.html', {'news': news_item})

