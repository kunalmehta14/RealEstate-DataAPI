from django.urls import path, include
from django.contrib import admin
from rest_framework import routers
from .views import (CitiesdataListAPIView, CitiesdataAPIView,
                    RealestatelistingListAPIView, RealestatelistingAPIView,
                    MortgagedataListAPIView, MortgagedataAPIView,
                    chatStartAPI, chatProcessAPI,
                    login, register, logout)

router = routers.DefaultRouter()
urlpatterns = router.urls

urlpatterns += [
    path('admin/', admin.site.urls),
    path('cities/', 
         CitiesdataListAPIView.as_view(), name='cities'),
    path('city/<str:cityname>/', 
         CitiesdataAPIView.as_view(), name='city-detail'),
    path('realestatelistings/', 
         RealestatelistingListAPIView.as_view(), name='listings'),
    path('realestatelistings/<str:pk>/', 
         RealestatelistingAPIView.as_view(), name='realestatelisting'),
    path('mortgagerates/',
         MortgagedataListAPIView.as_view(), name='mortgagerates'),
    path('mortgagerates/<str:lendername>',
         MortgagedataAPIView.as_view(), name='mortgagerate'),
    path('chat', 
          chatStartAPI, name='chat'),
     path('chat/<str:session>', 
          chatProcessAPI, name='chatsession'),
    path('login', 
          login, name='login'),
    path('register', 
          register, name='register'),
    path('logout', 
          logout, name='logout')
]