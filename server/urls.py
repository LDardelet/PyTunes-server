from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

import library
import playlist_manage

router = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path(
        'api-auth/', include('rest_framework.urls', namespace='rest_framework')
    ),
    path('data/', include('library.urls')),
    path('playlist/', include('playlist_manage.urls')),
]

