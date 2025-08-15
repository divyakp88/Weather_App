from django.urls import path
from .views import WeatherView,index
urlpatterns=[
    #path('',index,name='index'),
    path('',index,name='index'),
    path('api/weather/<str:city>/',WeatherView.as_view(),name='weather-api'),
]