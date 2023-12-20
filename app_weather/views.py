from datetime import datetime, timedelta

import yandex_weather_api

from django.http import HttpRequest, JsonResponse

import requests

from geopy.geocoders import Nominatim  # Подключаем библиотеку


def get_coordonats(sity: str):
    geolocator = Nominatim(user_agent="Tester")
    location = geolocator.geocode(sity)  # Создаем переменную, которая состоит из нужного нам адреса
    return location.latitude, location.longitude


last_requests = {}


def weather(request: HttpRequest):
    city_name = request.GET.get('city')
    if city_name:
        now = datetime.now()
        if city_name in last_requests and now - last_requests[city_name] < timedelta(minutes=30):

            return JsonResponse({'message': f'город {city_name} уже проверялся'}, status=200)
        else:
            last_requests[city_name] = now

            if not city_name:
                return JsonResponse({'error': 'Город не найден'}, status=400)
            latitude, longitude = get_coordonats(city_name)

            api_key = "c828a84c-1496-4a66-9e24-19183e20d6d9"  #
            try:
                weather_now = yandex_weather_api.get(api_key=api_key, session=requests, lat=latitude, lon=longitude)[
                    'fact']
                # my_json = {"obs_time": 1703005200.0, "temp": 7.0, "feels_like": 4.0, "icon": "ovc_ra", "condition": "cloudy-and-rain", "wind_speed": 3.0, "wind_dir": "w", "pressure_mm": 765.0, "pressure_pa": 1019.0, "humidity": 100.0, "daytime": "n", "polar": False, "season": "winter", "wind_gust": 4.2}
                return JsonResponse({'Город': city_name,
                                     'текущая температура': weather_now['temp'],
                                     'атмосферное давление': weather_now['pressure_mm'],
                                     'скорость ветра': weather_now['wind_speed'],
                                     })
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
