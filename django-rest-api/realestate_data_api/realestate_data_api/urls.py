from django.urls import path
from django.contrib import admin
from rest_framework import routers
from .views import (CitiesdataListAPIView, CitiesdataAPIView,
                    RemaxlistingsListAPIView)

router = routers.DefaultRouter()
urlpatterns = router.urls

urlpatterns += [
    path('admin/', admin.site.urls),
    path('cities/', CitiesdataListAPIView.as_view(), name='cities'),
    path('cities/<str:cityname>/', CitiesdataAPIView.as_view(), name='city-detail'),
    path('remaxlistings/', RemaxlistingsListAPIView.as_view(), name='remaxlistings')
]