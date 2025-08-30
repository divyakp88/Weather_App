from django.shortcuts import render
import requests
from requests.exceptions import RequestException
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from decouple import config
import logging
logger=logging.getLogger(__name__)


class WeatherView(APIView):
    logger.debug("Weather view called")
    def get(self,request,city):
        api_key=config("OPENWEATHER_API_KEY")
        
        base_url=config("BASE_URL1")
        params={
            'q':city,
            'appid':api_key,
            'units':'metric'
        }
        try:
            response=requests.get(base_url,params=params,timeout=10)
            response.raise_for_status()
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
        except requests.Timeout:
            logger.error("Weather API request time out")  
            return Response({'error':'Request Time out'},status=504)  
        except RequestException as e:
            return Response({'error':'Weather API request Failed','details':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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
        base_url=config('BASE_URL',default='http://127.0.0.1:8000')
        api_url=f'{base_url}/api/weather/{city}/'
        try:
            response=requests.get(api_url,timeout=10)
            response.raise_for_status()
            if response.status_code==200:
                data=response.json()
            else:
                error='City Not Found'
        except requests.Timeout:
            error = "Weather API took too long to respond"
        except requests.RequestException as e:
            error = f"Failed to fetch weather data: {e}"
    return render(request,'index.html',{'data':data,'error':error,'current_day':current_day,'current_date':current_date,'current_time':current_time})        



