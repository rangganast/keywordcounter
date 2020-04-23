from datetime import datetime
from django.db.models import Count
from rest_framework import serializers, mixins
from django.contrib.auth.models import User
from .models import Keyword, KeywordHistory

class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ('id', 'keyword', 'last_created')
        depth = 2


class KeywordHistorySerializer(serializers.ModelSerializer):
    keyword = serializers.CharField(source='keywords.keyword')

    class Meta:
        model = KeywordHistory
        fields = ('id', 'date_created', 'time_created', 'keyword')

    def create(self, validated_data):
        keyword = validated_data.pop('keywords')
        keyword_instance, created = Keyword.objects.get_or_create(keyword=keyword['keyword'].lower())
        if created:
            pass
        else:
            Keyword.objects.filter(keyword=keyword['keyword'].lower()).update(last_created=datetime.now())

        history_instance = KeywordHistory.objects.create(**validated_data, keywords=keyword_instance)
        return history_instance


class KeywordCountSerializer(serializers.ModelSerializer):
    keywords = KeywordHistorySerializer(many=True, read_only=True)

    keyword_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Keyword
        fields = ('keyword', 'keywords', 'keyword_count')