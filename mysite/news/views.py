from django.shortcuts import render
from .models import News, Country
from django.shortcuts import get_object_or_404
from django.db.models import Value as V
from django.db.models.functions import Length
from django.db.models.functions import Length

def home(request):
    latest_news = {}

    # Получаем список уникальных стран из базы данных
    countries = News.objects.values_list('country_name', flat=True).distinct()

    # Для каждой страны выбираем одну новость, удовлетворяющую условиям
    for country in countries:
        # Фильтруем новости по стране и условиям content_review
        country_news = News.objects.filter(
            country_name=country,
            content_review__isnull=False,  # не пустая
        ).exclude(
            content_review__lt=200,  # Содержимое обзора менее 200 символов
            content_review__icontains="Error"  # Содержимое обзора начинается с "Error"
        ).order_by('-searches').first()  # Сортируем по количеству просмотров

        if country_news:
            latest_news[country] = country_news

    return render(request, 'home.html', {'latest_news': latest_news})


def country_news(request, country_name):
    country = get_object_or_404(Country, name=country_name)
    # Сортировка сначала по дате (новые вначале), затем по searches (убывание)
    news_list = (
        News.objects.annotate(content_length=Length('content_review'))
        .filter(
            country_name=country,
            content_review__isnull=False,
            content_review__gt=V('')  # Исключаем пустые значения
        )
        .exclude(content_review__istartswith='Error')
        .exclude(content_review__exact='')
        .filter(content_length__gt=200)
        .order_by('-date', '-searches')[:20]
    )
    return render(request, 'country_news.html', {'news_list': news_list, 'country': country})



def news_detail(request, country_name, news_id):
    news = get_object_or_404(News, pk=news_id)
    country = get_object_or_404(Country, name=country_name)
    arabic_countries = ['Saudi Arabia', 'Israel', 'Egypt']
    return render(request, 'news_detail.html', {'news': news, 'country': country, 'arabic_countries': arabic_countries})
