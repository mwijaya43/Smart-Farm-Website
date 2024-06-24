from django.contrib import admin
from .models import EcosystemSensor, EcosystemActuator, SmartPlantingSensor, SmartPlantingActuator, FarmManagementSensor, FarmManagementActuator

# Register your models here.

@admin.register(EcosystemSensor)
class EcosystemSensorAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'timestamp')
    search_fields = ('name', 'value')

@admin.register(EcosystemActuator)
class EcosystemActuatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'timestamp')
    search_fields = ('name', 'value')

@admin.register(SmartPlantingSensor)
class SmartPlantingSensorAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'timestamp')
    search_fields = ('name', 'value')

@admin.register(SmartPlantingActuator)
class SmartPlantingActuatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'timestamp')
    search_fields = ('name', 'value')

@admin.register(FarmManagementSensor)
class FarmManagementSensorAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'timestamp')
    search_fields = ('name', 'value')

@admin.register(FarmManagementActuator)
class FarmManagementActuatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'value', 'timestamp')
    search_fields = ('name', 'value')
