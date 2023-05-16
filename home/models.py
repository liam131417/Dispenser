from django.db import models

class Dispenser(models.Model):
    name = models.CharField(max_length=50)
    medicine_name = models.CharField(max_length=50)
