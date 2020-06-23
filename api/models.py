from django.db import models

class Keyword(models.Model):
    keyword = models.TextField()
    last_created = models.DateTimeField(auto_now_add=True)
    lastscrape_date = models.DateField(blank=True, null=True)
    lastscrape_time = models.TimeField(blank=True, null=True)
    lastscrape_products = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.keyword

class KeywordHistory(models.Model):
    keywords = models.ForeignKey(Keyword, on_delete=models.CASCADE, related_name='keywords')
    keyword_ip = models.CharField(max_length=20, null=True, blank=True, default=None)
    source = models.CharField(max_length=50, null=True, blank=True, default=None)
    date_created = models.DateField(auto_now_add=True)
    time_created = models.TimeField(auto_now_add=True)