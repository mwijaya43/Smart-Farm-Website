from django.db import models

# Create your models here.
class EcosystemSensor(models.Model):
    name = models.CharField(max_length=100)
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

class EcosystemActuator(models.Model):
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=10, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class SmartPlantingSensor(models.Model):
    name = models.CharField(max_length=100)
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

class SmartPlantingActuator(models.Model):
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=10, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class FarmManagementSensor(models.Model):
    name = models.CharField(max_length=100)
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

class FarmManagementActuator(models.Model):
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=10, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class SmartPlantingActSens(models.Model):
    waterlevelvalue = models.FloatField(null=True)
    nutrisiTDSvalue = models.FloatField(null=True)
    pHvalue = models.FloatField(null=True)
    pompaairvalue = models.CharField(max_length=10, null=True, blank=True)
    nutrisivalue = models.CharField(max_length=10, null=True, blank=True)
    dispenservalue = models.CharField(max_length=10, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class EcosystemActSens(models.Model):
    suhuvalue = models.FloatField(null=True)
    kelembapanvalue = models.FloatField(null=True)
    intensitascahayavalue = models.FloatField(null=True)
    kipasvalue = models.CharField(max_length=10, null=True, blank=True)
    watersprinklervalue = models.CharField(max_length=10, null=True, blank=True)
    lampuUVvalue = models.CharField(max_length=10, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class FarmManagementActSens(models.Model):
    ultrasonicvalue = models.FloatField(null=True)
    kameravalue = models.FloatField(null=True)
    LIDARvalue = models.FloatField(null=True)
    LCDvalue = models.CharField(max_length=10, null=True, blank=True)
    LEDRGBvalue = models.CharField(max_length=10, null=True, blank=True)
    alarmvalue = models.CharField(max_length=10, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)