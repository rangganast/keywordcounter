from rest_framework import routers
from . import views

router = routers.SimpleRouter(trailing_slash=False)

router.register('list', views.KeywordListViewSet)
router.register('search', views.KeywordHistoryViewSet)
router.register('count', views.KeywordCountViewSet)
router.register('ip', views.KeywordIpDetailViewSet)
router.register('scrape', views.KeywordStatViewSet)
router.register('ajax/load-regions', views.LoadRegionsViewset)
