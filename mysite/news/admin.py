from django.contrib import admin
from .models import News, Country

# Регистрация модели News
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'country', 'published_date')
    list_filter = ('country', 'published_date')
    search_fields = ('title', 'content')

# Регистрация модели Country
@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)
