from django.contrib import admin
from django.urls import path
from  .views import weather

app_name = 'app_weather'
urlpatterns = [
path('', weather, name='index')

]
