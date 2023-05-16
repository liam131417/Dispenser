from django.db import models
from django.utils import timezone

# Create your models here.
class HumiditySensor(models.Model):
    id = models.IntegerField(primary_key=True)
    temperature = models.CharField(max_length=10)
    humidity = models.CharField(max_length=10)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        app_label = 'sensors'

class MotionSensor(models.Model):
    id = models.IntegerField(primary_key=True)
    motion = models.CharField(max_length=10)
    created_at = models.DateTimeField(default=timezone.now)
    class Meta:
        app_label = 'sensors'
class UltrasonicSensor(models.Model):
    id = models.IntegerField(primary_key=True)
    distance = models.CharField(max_length=10)
    created_at = models.DateTimeField(default=timezone.now)
    class Meta:
        app_label = 'sensors'

class MedicalDispensor(models.Model):
    id = models.IntegerField(primary_key=True)
    isDispensing = models.BooleanField(default = False)
    medicine = models.CharField(max_length=100,null=True)
    ultraId = models.IntegerField(default=1000)
    tempId = models.IntegerField(default=1000)
    created_at = models.DateTimeField(default=timezone.now)
    class Meta:
        app_label = 'sensors'



