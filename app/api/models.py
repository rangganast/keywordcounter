from django.db import models


class Keyword(models.Model):
    keyword = models.CharField(max_length=30)
    last_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.keyword


class KeywordHistory(models.Model):
    keywords = models.ForeignKey(Keyword, on_delete=models.CASCADE, related_name='keywords')
    date_created = models.DateField(auto_now_add=True)
    time_created = models.TimeField(auto_now_add=True)
