from rest_framework import routers
from .views import KeywordHistoryViewSet, KeywordCountViewSet, KeywordListViewSet, KeywordStatViewSet

router = routers.SimpleRouter(trailing_slash=False)

router.register('list', KeywordListViewSet)
router.register('search', KeywordHistoryViewSet)
router.register('count', KeywordCountViewSet)
router.register('scrape', KeywordStatViewSet)
