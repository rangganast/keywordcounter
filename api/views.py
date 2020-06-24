import datetime
from rest_framework import status
from django.db.models import Count, Q, Value, CharField, F, Subquery, Max, Min, OuterRef
from django.http import JsonResponse
from rest_framework import viewsets, mixins
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .models import Keyword, KeywordHistory
from .serializers import KeywordSerializer, KeywordHistorySerializer, KeywordCountSerializer, KeywordStatSerializer, KeywordIpDetailSerializer, LoadRegionsSerializer

class KeywordListViewSet(viewsets.ModelViewSet):
    queryset = Keyword.objects.all().order_by('pk')
    serializer_class = KeywordSerializer
    permission_classes = [DjangoModelPermissions]
    http_method_names = ['get', 'head']

class KeywordStatViewSet(viewsets.ModelViewSet):
    queryset = Keyword.objects.all().order_by('pk')
    serializer_class = KeywordStatSerializer
    permission_classes = [DjangoModelPermissions]
    http_method_names = ['post', 'head']

class KeywordHistoryViewSet(viewsets.ModelViewSet):
    queryset = KeywordHistory.objects.all().order_by('pk')
    serializer_class = KeywordHistorySerializer
    permission_classes = [DjangoModelPermissions]
    http_method_names = ['get', 'post', 'head']

class KeywordCountViewSet(viewsets.ModelViewSet):
    queryset = Keyword.objects.all().order_by('pk')
    serializer_class = KeywordCountSerializer
    permission_classes = [DjangoModelPermissions]
    http_method_names = ['get', 'head']

    def list(self, request, *args, **kwargs):
        keywords = Keyword.objects.filter(keywords__date_created__range=[datetime.date.today() - datetime.timedelta(days=30), datetime.date.today()]).distinct()
        jsonlist = []
        for keyword in keywords:
            queryset = KeywordHistory.objects.filter(keywords=keyword.id, date_created__range=[datetime.date.today() - datetime.timedelta(days=30), datetime.date.today()]).values('keyword_ip').annotate(
                id=F('keywords__id'),
                keyword_count=Count('keyword_ip')
                ).order_by('-keyword_count')
            jsonlist.append(queryset[0])

        queryset = list(Keyword.objects.filter(keywords__date_created__range=[datetime.date.today() - datetime.timedelta(days=30), datetime.date.today()]).values('keyword').annotate(
            id=F('id'),
            lastscrape_date=F('lastscrape_date'),
            lastscrape_time=F('lastscrape_time'),
            lastscrape_products=F('lastscrape_products'),
            keyword_count=Count('keywords__id'),
            holahalo_website=Count('keywords__source', filter=Q(keywords__source='Holahalo Website')),
            holahalo_mobile_website=Count('keywords__source', filter=Q(keywords__source='Holahalo Mobile Website')),
            holahalo_android=Count('keywords__source', filter=Q(keywords__source='Holahalo Android'))
            ).order_by('-last_created'))

        for query in queryset:
            if query['lastscrape_date']:
                query['lastscrape_date'] = datetime.datetime.strptime(str(query['lastscrape_date']), '%Y-%m-%d').strftime('%d-%m-%Y')
            query['keyword_ip'] = list(filter(lambda x: x["id"] == query['id'], jsonlist))[0]['keyword_ip']

        date1 = self.request.GET.get("date1")
        date2 = self.request.GET.get("date2")

        if date1 is not None:
            date1 = datetime.datetime.strptime(date1, '%d-%m-%Y')
            date1 = date1.strftime('%Y-%m-%d')

            date2 = datetime.datetime.strptime(date2, '%d-%m-%Y')
            date2 = date2.strftime('%Y-%m-%d')

            keywords = Keyword.objects.filter(keywords__date_created__range=[date1, date2]).distinct()
            jsonlist = []
            for keyword in keywords:
                queryset = KeywordHistory.objects.filter(keywords=keyword.id, date_created__range=[date1, date2]).values('keyword_ip').annotate(
                    keyword_id=F('keywords__id'),
                    keyword_count=Count('keyword_ip')
                    ).order_by('-keyword_count')
                jsonlist.append(queryset[0])

            queryset = list(Keyword.objects.filter(keywords__date_created__range=[date1, date2]).values('keyword').annotate(
                keyword_id=F('id'),
                keyword_count=Count('keywords__id'),
                holahalo_website=Count('keywords__source', filter=Q(keywords__source='Holahalo Website')),
                holahalo_mobile_website=Count('keywords__source', filter=Q(keywords__source='Holahalo Mobile Website')),
                holahalo_android=Count('keywords__source', filter=Q(keywords__source='Holahalo Android'))
                ).order_by('-last_created'))

            for query in queryset:
                query['keyword_ip'] = list(filter(lambda x: x["keyword_id"] == query['keyword_id'], jsonlist))[0]['keyword_ip']

        return JsonResponse(queryset, safe=False)

class KeywordIpDetailViewSet(viewsets.ModelViewSet):
    queryset = KeywordHistory.objects.all().order_by('pk')
    serializer_class = KeywordIpDetailSerializer
    permission_classes = [DjangoModelPermissions]
    http_method_names = ['get', 'head']

    def retrieve(self, request, pk):
        queryset = list(KeywordHistory.objects.filter(keywords=pk).values('keyword_ip').annotate(
            keyword=F('keywords__keyword'),
            keyword_ip_country_id=F('keyword_ip_country_id'),
            keyword_ip_country=F('keyword_ip_country'),
            keyword_ip_region=F('keyword_ip_region'),
            keyword_ip_city=F('keyword_ip_city'),
            count=Count('keyword_ip'),
            ).order_by('-count'))
        
        if not queryset:
            return JsonResponse({'detail' : 'not found'}, safe=False)

        return JsonResponse(queryset, safe=False)

class LoadRegionsViewset(viewsets.ModelViewSet):
    queryset = KeywordHistory.objects.all().order_by('pk')
    serializer_class = LoadRegionsSerializer
    permission_classes = [DjangoModelPermissions]
    http_method_names = ['get', 'head']

    def get_queryset(self):
        country = self.request.GET.get('country')
        pk = self.request.GET.get('keyword_id')

        queryset = KeywordHistory.objects.filter(keywords=pk, keyword_ip_country=country)

        return queryset
        