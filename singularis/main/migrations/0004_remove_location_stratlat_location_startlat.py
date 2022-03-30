# Generated by Django 4.0.1 on 2022-03-07 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='stratlat',
        ),
        migrations.AddField(
            model_name='location',
            name='startlat',
            field=models.IntegerField(blank=True, null=True, verbose_name='Latitude'),
        ),
    ]
