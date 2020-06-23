import pytz
import json
import urllib
import pycountry
from urllib.request import urlopen
from django.utils import timezone
from django.db.models import Count
from django.http import JsonResponse
from rest_framework import serializers, mixins
from django.contrib.auth.models import User
from .models import Keyword, KeywordHistory


class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ('id', 'keyword', 'last_created')
        depth = 1

class KeywordStatSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = Keyword
        fields = ('id', 'lastscrape_date', 'lastscrape_time', 'lastscrape_products')

    def create(self, validated_data):
        keyword_id = validated_data['id']
        keyword_instance = Keyword.objects.get(id=keyword_id)

        keyword_instance.lastscrape_date = validated_data['lastscrape_date']
        keyword_instance.lastscrape_time = validated_data['lastscrape_time']
        keyword_instance.lastscrape_products = validated_data['lastscrape_products']
        keyword_instance.save()

        return keyword_instance

class KeywordHistorySerializer(serializers.ModelSerializer):
    keyword = serializers.CharField(source='keywords.keyword')

    class Meta:
        model = KeywordHistory
        fields = ('id', 'date_created', 'time_created', 'keyword', 'keyword_ip', 'source')

    def create(self, validated_data):
        keyword = validated_data.pop('keywords')
        keyword_instance, created = Keyword.objects.get_or_create(keyword=keyword['keyword'].lower())
        if created:
            pass
        else:
            Keyword.objects.filter(keyword=keyword['keyword'].lower()).update(last_created=timezone.now())

        # keyword_ip = validated_data.pop('keyword_ip')
        # if keyword_ip:
        #     url = 'https://ipinfo.io/' + keyword_ip + '/json'
        #     try:
        #         res = urllib.request.urlopen(url)
        #         data = json.load(res)
        #         if data['country']:
        #             validated_data['keyword_ip'] = pycountry.countries.get(alpha_2=data['country']).name
        #         else:
        #             validated_data['keyword_ip'] = None

        #     except urllib.error.HTTPError:
        #         validated_data['keyword_ip'] = None
        # else:
        #     pass
        

        history_instance = KeywordHistory.objects.create(**validated_data, keywords=keyword_instance)
        return history_instance


class KeywordCountSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    keyword = serializers.CharField(read_only=True)
    keyword_count = serializers.IntegerField(read_only=True)
    keyword_ip = serializers.CharField(read_only=True)
    holahalo_website = serializers.IntegerField(read_only=True)
    holahalo_mobile_website = serializers.IntegerField(read_only=True)
    holahalo_android = serializers.IntegerField(read_only=True)

    class Meta:
        model = Keyword
        fields = ('id', 'keyword', 'keyword_ip', 'holahalo_website', 'holahalo_mobile_website', 'holahalo_android', 'lastscrape_date', 'lastscrape_time', 'lastscrape_products', 'keyword_count')