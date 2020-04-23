from django.contrib import admin
from django.urls import path, include
from api.router import router
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='admin/', permanent=False), name='home'),
    path('admin/', admin.site.urls),
    path('api/v1/keyword/', include(router.urls)),
]
