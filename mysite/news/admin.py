from django.contrib import admin
from .models import News, Country

# Регистрация модели News
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'country_name', 'date')
    list_filter = ('country_name', 'date')
    search_fields = ('title', 'description')
    
# Регистрация модели Country
@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)
