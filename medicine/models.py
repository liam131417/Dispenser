from django.db import models

# Create your models here.

class MedicineDetail(models.Model):
    name = models.CharField(primary_key=True,max_length=100,unique=True)
    condition = models.CharField(max_length=100)
    alcohol = models.CharField(max_length=1)
    pregnant = models.CharField(max_length=1)
    rating = models.FloatField(default=0.0)
    rx_otc = models.CharField(max_length=50)
    side_effects = models.TextField()
    class Meta:
        app_label = 'medicine'
