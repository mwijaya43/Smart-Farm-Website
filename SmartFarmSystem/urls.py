from django.urls import path, include
from . import views as views

app_name = 'SmartFarmSystem'

urlpatterns =   [path('', views.SmartFarmSystemLoop, name='SmartFarmSystemLoop'),
                path('info/', views.SmartFarmSystemInformation, name='SmartFarmSystemInformation'),
                path('fetch_sensor_data/', views.fetch_sensor_data, name='fetch_sensor_data'),
                path('trigger-smart-farm-loop/', views.trigger_smart_farm_loop, name='trigger_smart_farm_loop'),
                path('ecosystemlog/', views.ecosystem_log, name='ecosystemlog'),
                path('smartplantinglog/', views.smart_planting_log, name='smartplantinglog'),
                path('farmmanagementlog/', views.farm_management_log, name='farmmanagementlog'),
                ]