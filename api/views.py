import datetime
from django.db.models import Count, Q, Value, CharField, F, Func, Max
from django.db.models.functions import Concat
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework import viewsets, mixins
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from drf_renderer_xlsx.mixins import XLSXFileMixin
from drf_renderer_xlsx.renderers import XLSXRenderer
from .models import Keyword, KeywordHistory
from . import serializers

class KeywordListViewSet(viewsets.ModelViewSet):
    queryset = Keyword.objects.all().order_by('pk')
    serializer_class = serializers.KeywordSerializer
    permission_classes = [DjangoModelPermissions]
    http_method_names = ['get', 'head']

class KeywordStatViewSet(viewsets.ModelViewSet):
    queryset = Keyword.objects.all().order_by('pk')
    serializer_class = serializers.KeywordStatSerializer
    permission_classes = [DjangoModelPermissions]
    http_method_names = ['post', 'head']

class KeywordHistoryViewSet(viewsets.ModelViewSet):
    queryset = KeywordHistory.objects.all().order_by('pk')
    serializer_class = serializers.KeywordHistorySerializer
    permission_classes = [DjangoModelPermissions]
    http_method_names = ['get', 'post', 'head']

class KeywordCountViewSet(viewsets.ModelViewSet):
    queryset = Keyword.objects.all().order_by('pk')
    serializer_class = serializers.KeywordCountSerializer
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
            lastscrape_date=Func(F('lastscrape_date'), Value('dd-MM-yyyy'), function='to_char', outputfield=CharField()),
            lastscrape_time=F('lastscrape_time'),
            lastscrape_products=F('lastscrape_products'),
            keyword_count=Count('keywords__id'),
            holahalo_website=Count('keywords__source', filter=Q(keywords__source='Holahalo Website')),
            holahalo_mobile_website=Count('keywords__source', filter=Q(keywords__source='Holahalo Mobile Website')),
            holahalo_android=Count('keywords__source', filter=Q(keywords__source='Holahalo Android'))
            ).order_by('-last_created'))

        for query in queryset:
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
                    id=F('keywords__id'),
                    keyword_count=Count('keyword_ip')
                    ).order_by('-keyword_count')
                jsonlist.append(queryset[0])

            queryset = list(Keyword.objects.filter(keywords__date_created__range=[date1, date2]).values('keyword').annotate(
                id=F('id'),
                lastscrape_date=Func(F('lastscrape_date'), Value('dd-MM-yyyy'), function='to_char', outputfield=CharField()),
                lastscrape_time=F('lastscrape_time'),
                lastscrape_products=F('lastscrape_products'),
                keyword_count=Count('keywords__id'),
                holahalo_website=Count('keywords__source', filter=Q(keywords__source='Holahalo Website')),
                holahalo_mobile_website=Count('keywords__source', filter=Q(keywords__source='Holahalo Mobile Website')),
                holahalo_android=Count('keywords__source', filter=Q(keywords__source='Holahalo Android'))
                ).order_by('-last_created'))

            for query in queryset:
                query['keyword_ip'] = list(filter(lambda x: x["id"] == query['id'], jsonlist))[0]['keyword_ip']

        return JsonResponse(queryset, safe=False) 

class KeywordIpDetailViewSet(viewsets.ModelViewSet):
    queryset = KeywordHistory.objects.all().order_by('pk')
    serializer_class = serializers.KeywordIpDetailSerializer
    permission_classes = [DjangoModelPermissions]
    http_method_names = ['get', 'head']

    def retrieve(self, request, pk):
        queryset = list(KeywordHistory.objects.filter(keywords=pk).values('keyword_ip').annotate(
            keyword=F('keywords__keyword'),
            keyword_ip_country_id=F('keyword_ip_country_id'),
            keyword_ip_country=F('keyword_ip_country'),
            keyword_ip_region=F('keyword_ip_region'),
            keyword_ip_city=F('keyword_ip_city'),
            count=Count('keywords__keyword'),
            ).order_by('-count'))

        date1 = self.request.GET.get("date1")
        date2 = self.request.GET.get("date2")

        if date1 is not None:
            queryset = list(KeywordHistory.objects.filter(keywords=pk, date_created__range=[date1, date2]).values('keyword_ip').annotate(
            keyword=F('keywords__keyword'),
            keyword_ip_country_id=F('keyword_ip_country_id'),
            keyword_ip_country=F('keyword_ip_country'),
            keyword_ip_region=F('keyword_ip_region'),
            keyword_ip_city=F('keyword_ip_city'),
            count=Count('keywords__keyword'),
            ).order_by('-count'))
        
        if not queryset:
            return JsonResponse({'detail' : 'not found'}, safe=False)

        return JsonResponse(queryset, safe=False)

class LoadRegionsViewSet(viewsets.ModelViewSet):
    queryset = KeywordHistory.objects.all().order_by('pk')
    serializer_class = serializers.LoadRegionsSerializer
    permission_classes = [DjangoModelPermissions]
    http_method_names = ['get', 'head']

    def get_queryset(self):
        country = self.request.GET.get('country')
        pk = self.request.GET.get('keyword_id')

        queryset = KeywordHistory.objects.filter(keywords=pk, keyword_ip_country=country)

        return queryset

class LoadCitiesViewSet(viewsets.ModelViewSet):
    queryset = KeywordHistory.objects.all().order_by('pk')
    serializer_class = serializers.LoadCitiesSerializer
    permission_classes = [DjangoModelPermissions]
    http_method_names = ['get', 'head']

    def get_queryset(self):
        country = self.request.GET.get('country')
        region = self.request.GET.get('region')
        pk = self.request.GET.get('keyword_id')

        queryset = KeywordHistory.objects.filter(keywords=pk, keyword_ip_country=country, keyword_ip_region=region)

        return queryset

class ExportExcelViewset(XLSXFileMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Keyword.objects.all()
    serializer_class = serializers.XLSXExportSerializer
    renderer_classes = [XLSXRenderer]
    column_header = {
        'titles' : [
            "Keyword",
            "Sumber Keyword",
            "IP Pencarian",
            "Jumlah Pencarian Keyword",
            "Tanggal",
            "Jam",
            "Jumlah Total Produk",
        ],
        'column_width': [20, 40, 20, 40, 20, 20, 20],
        'height' : 20,
        'style' : {
            'fill': {
                'fill_type': 'solid',
                'start_color': 'CCCCCC',
            },
            'border_side': {
                'border_style': 'thin',
                'color': 'FF000000',
            },
            'font': {
                'name': 'Calibri',
                'size': 11,
                'bold': True,
                'color': 'FF000000',
            },
        }
    }
    body = {
        'style' : {
            'border_side': {
                'border_style': 'thin',
                'color': 'FF000000',
            },
            'alignment': {
                'vertical': 'center',
                'horizontal': 'center',
                'wrapText': True,
                'shrinkToFit' : True,
            }
        },
        'height' : 60,
    }
    filename = 'keywords.xlsx'

    def get_queryset(self):
        date1 = self.request.GET.get("date1")
        date2 = self.request.GET.get("date2")

        keywords = Keyword.objects.filter(keywords__date_created__range=[date1, date2]).distinct().order_by('-last_created')
        jsonlist = []
        for keyword in keywords:
            queryset = KeywordHistory.objects.filter(keywords=keyword.id, date_created__range=[datetime.date.today() - datetime.timedelta(days=30), datetime.date.today()]).values('keyword_ip').annotate(
                id=F('keywords__id'),
                keyword_count=Count('keyword_ip')
                ).order_by('-keyword_count')
            jsonlist.append(queryset[0])

        qs = None
        for index, value in enumerate(jsonlist):
            queryset = Keyword.objects.filter(id=value['id'], keywords__date_created__range=[date1, date2]).values('keyword').annotate(
                    lastscrape_date=Func(F('lastscrape_date'), Value('dd-MM-yyyy'), function='to_char', output_field=CharField()),
                    lastscrape_time=F('lastscrape_time'),
                    lastscrape_products=F('lastscrape_products'),
                    keyword_ip=Value(value['keyword_ip'], output_field=CharField()),
                    keyword_count=Count('keywords__id'),
                    last_created=F('last_created'),
                    source=Concat(
                        Value('Holahalo Website: '),
                        Count('keywords__source', filter=Q(keywords__source='Holahalo Website')),
                        Value('\nHolahalo Mobile Website: '),
                        Count('keywords__source', filter=Q(keywords__source='Holahalo Mobile Website')),
                        Value('\nHolahalo Android: '),
                        Count('keywords__source', filter=Q(keywords__source='Holahalo Android')),
                        output_field=CharField()),
                    )

            if index == 0:
                qs = queryset
            else:
                qs = qs.union(queryset, all=False)

        return qs.order_by('-last_created')