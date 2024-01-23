from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'news_country'

    def __str__(self):
        return self.name

class News(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    country_name = models.CharField(max_length=100)
    searches = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'news'
            
    def __str__(self):
        return self.title


