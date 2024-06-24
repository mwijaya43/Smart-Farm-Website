# Generated by Django 4.2.7 on 2023-12-07 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SmartFarmSystem', '0002_ecosystemactsens_farmmanagementactsens_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ecosystemactsens',
            old_name='actuatorvalue',
            new_name='kipasvalue',
        ),
        migrations.RenameField(
            model_name='farmmanagementactsens',
            old_name='actuatorvalue',
            new_name='LCDvalue',
        ),
        migrations.RenameField(
            model_name='smartplantingactsens',
            old_name='actuatorvalue',
            new_name='dispenservalue',
        ),
        migrations.RemoveField(
            model_name='ecosystemactsens',
            name='actuatorname',
        ),
        migrations.RemoveField(
            model_name='ecosystemactsens',
            name='sensorname',
        ),
        migrations.RemoveField(
            model_name='ecosystemactsens',
            name='sensorvalue',
        ),
        migrations.RemoveField(
            model_name='farmmanagementactsens',
            name='actuatorname',
        ),
        migrations.RemoveField(
            model_name='farmmanagementactsens',
            name='sensorname',
        ),
        migrations.RemoveField(
            model_name='farmmanagementactsens',
            name='sensorvalue',
        ),
        migrations.RemoveField(
            model_name='smartplantingactsens',
            name='actuatorname',
        ),
        migrations.RemoveField(
            model_name='smartplantingactsens',
            name='sensorname',
        ),
        migrations.RemoveField(
            model_name='smartplantingactsens',
            name='sensorvalue',
        ),
        migrations.AddField(
            model_name='ecosystemactsens',
            name='intensitascahayavalue',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='ecosystemactsens',
            name='kelembapanvalue',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='ecosystemactsens',
            name='lampuUVvalue',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='ecosystemactsens',
            name='suhuvalue',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='ecosystemactsens',
            name='watersprinklervalue',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='farmmanagementactsens',
            name='LEDRGBvalue',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='farmmanagementactsens',
            name='LIDARvalue',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='farmmanagementactsens',
            name='alarmvalue',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='farmmanagementactsens',
            name='kameravalue',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='farmmanagementactsens',
            name='ultrasonicvalue',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='smartplantingactsens',
            name='nutrisiTDSvalue',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='smartplantingactsens',
            name='nutrisivalue',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='smartplantingactsens',
            name='pHvalue',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='smartplantingactsens',
            name='pompaairvalue',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='smartplantingactsens',
            name='waterlevelvalue',
            field=models.FloatField(null=True),
        ),
    ]
