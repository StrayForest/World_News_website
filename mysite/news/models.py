from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        managed = False  # Это отключит управление созданием таблицы Django
        db_table = 'news_country'

    def __str__(self):
        return self.name


class News(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    country_name = models.CharField(max_length=100)
    searches = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    content_review = models.TextField()

    class Meta:
        db_table = 'news'
        indexes = [
            models.Index(fields=['country_name']),
            models.Index(fields=['searches']),
            models.Index(fields=['date']),
            # Другие индексы по необходимости
        ]

    def __str__(self):
        return self.title
