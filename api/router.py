from rest_framework import routers
from .views import KeywordHistoryViewSet, KeywordCountViewSet, KeywordListViewSet

router = routers.DefaultRouter()

router.register('list', KeywordListViewSet)
router.register('search', KeywordHistoryViewSet)
router.register('count', KeywordCountViewSet)
