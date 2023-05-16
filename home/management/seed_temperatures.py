from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random
from dispensor.sensors.models import HumiditySensor  # adjust the import based on your project structure
from dispensor.sensors.models import UltrasonicSensor  # adjust the import based on your project structure

class Command(BaseCommand):
    help = 'Seeds the database with 365 temperature records'
    y = timezone.now
    def handle(self, *args, **options):
        for i in range(365):
            y=y-timedelta(days=1)
            HumiditySensor.objects.create(
                id = 365-i,
                temperature=random.uniform(26, 32),
                created_at=y,
                humidity =random.uniform(40,85)
            )
            UltrasonicSensor.object.create(
                id = 365-i,
                distance = random.uniform(0,22),
                created_at = y
            )