from django.contrib import admin
from .models import Keyword, KeywordHistory


class KeywordAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'last_created')


admin.site.register(Keyword, KeywordAdmin)


class KeywordHistoryAdmin(admin.ModelAdmin):
    list_display = ('keywords', 'date_created', 'time_created')


admin.site.register(KeywordHistory, KeywordHistoryAdmin)
