from django.contrib import admin
from django.urls import path, include
from api.router import router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/keyword/', include(router.urls)),
]
