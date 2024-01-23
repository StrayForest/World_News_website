from django.shortcuts import render
from .models import News, Country
from django.shortcuts import get_object_or_404

def home(request):
    countries = Country.objects.all()
    latest_news = {}
    for country in countries:
        news = News.objects.filter(country_name=country).order_by('date').first()
        if news:
            latest_news[country] = news

    return render(request, 'home.html', {'latest_news': latest_news})


def get_top_news_by_country(country_name):
    return News.objects.filter(country_name=country_name)
def country_news(request, country_name):
    country = get_object_or_404(Country, name=country_name)
    news_list = News.objects.filter(country_name=country).order_by('-date')
    for news in news_list:
        print(news.title)  # Вывод заголовков новостей
    return render(request, 'country_news.html', {'news_list': news_list, 'country': country})



def news_detail(request, news_id):
    news_item = get_object_or_404(News, id=news_id)
    return render(request, 'news_detail.html', {'news': news_item})

