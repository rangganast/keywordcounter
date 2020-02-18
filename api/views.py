from datetime import datetime
from django.db.models import Count, Q
from rest_framework import viewsets, mixins
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .models import Keyword, KeywordHistory
from .serializers import KeywordSerializer, KeywordHistorySerializer, KeywordCountSerializer


class KeywordListViewSet(viewsets.ModelViewSet):
    queryset = Keyword.objects.all().order_by('pk')
    serializer_class = KeywordSerializer
    permission_classes = [DjangoModelPermissions]
    http_method_names = ['get', 'head']


class KeywordHistoryViewSet(viewsets.ModelViewSet):
    queryset = KeywordHistory.objects.all().order_by('pk')
    serializer_class = KeywordHistorySerializer
    permission_classes = [DjangoModelPermissions]
    http_method_names = ['get', 'post', 'head']


class KeywordCountViewSet(viewsets.ModelViewSet):
    queryset = Keyword.objects.values('keyword').annotate(
        keyword_count=Count('keywords__id')).order_by('-keyword_count')
    serializer_class = KeywordCountSerializer
    permission_classes = [DjangoModelPermissions]
    http_method_names = ['get', 'head']

    def get_queryset(self):
        queryset = Keyword.objects.values('keyword').annotate(
            keyword_count=Count('keywords__id')).order_by('-keyword_count')
        date1 = self.request.GET.get("date1")
        date2 = self.request.GET.get("date2")

        if date1 is not None:
            date1 = datetime.strptime(date1, '%d/%m/%Y')
            date1 = date1.strftime('%Y-%m-%d')

            date2 = datetime.strptime(date2, '%d/%m/%Y')
            date2 = date2.strftime('%Y-%m-%d')

            queryset = Keyword.objects.filter(keywords__date_created__range=[date1, date2]).values('keyword').annotate(
                keyword_count=Count('keywords__id')).order_by('-keyword_count')

        return queryset
