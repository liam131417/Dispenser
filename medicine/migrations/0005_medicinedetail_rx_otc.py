# Generated by Django 4.2.1 on 2023-05-08 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicine', '0004_alter_medicinedetail_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicinedetail',
            name='rx_otc',
            field=models.CharField(max_length=50),
        ),
    ]