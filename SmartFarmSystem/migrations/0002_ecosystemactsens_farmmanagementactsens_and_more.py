# Generated by Django 4.2.7 on 2023-12-06 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SmartFarmSystem', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EcosystemActSens',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sensorname', models.CharField(max_length=100)),
                ('sensorvalue', models.FloatField()),
                ('actuatorname', models.CharField(max_length=100)),
                ('actuatorvalue', models.CharField(blank=True, max_length=10, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='FarmManagementActSens',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sensorname', models.CharField(max_length=100)),
                ('sensorvalue', models.FloatField()),
                ('actuatorname', models.CharField(max_length=100)),
                ('actuatorvalue', models.CharField(blank=True, max_length=10, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SmartPlantingActSens',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sensorname', models.CharField(max_length=100)),
                ('sensorvalue', models.FloatField()),
                ('actuatorname', models.CharField(max_length=100)),
                ('actuatorvalue', models.CharField(blank=True, max_length=10, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
