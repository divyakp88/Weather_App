from django.shortcuts import render
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
class WeatherView(APIView):
    def get(self,request,city):
        api_key='66456c4f379fdcebb886750aeecb34f8'
        base_url='https://api.openweathermap.org/data/2.5/weather'
        params={
            'q':city,
            'appid':api_key,
            'units':'metric'
        }
        response=requests.get(base_url,params=params)
        if response.status_code==200:
            data=response.json()
            result={
                'city':data['name'],
                'temperature':data['main']['temp'],
                'description':data['weather'][0]['description'],
                'humidity':data['main']['humidity'],
                'coordinates':{
                    'longitude':data['coord']['lon'],
                    'lattitude':data['coord']['lat']
                },
                'temperature_min':data['main']['temp_min'],
                'temperature_max':data['main']['temp_max'],
                'sea_level':data['main'].get('sea_level','N/A'),
                'wind_speed':data['wind']['speed']
            }   
            return Response(result)     
        else:
            return Response({'error':'City Not Found'},status=status.HTTP_404_NOT_FOUND)

# front end view
def index(request):
    data=None
    error=None
    current_date=""
    current_day=""
    current_time=""
    now=datetime.now()
    if request.method=='POST':
        current_day=now.strftime("%A")
        current_date=now.strftime("%#d%b")
        current_time=now.strftime("%I:%M%p")
        city=request.POST.get('city')
        api_url=f'http://127.0.0.1:8000/api/weather/{city}/'
        response=requests.get(api_url)
        if response.status_code==200:
            data=response.json()
        else:
            error='City Not Found'
    return render(request,'index.html',{'data':data,'error':error,'current_day':current_day,'current_date':current_date,'current_time':current_time})        



