# Generated by Django 4.0.1 on 2022-03-29 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_countries'),
    ]

    operations = [
        migrations.AddField(
            model_name='routecoordinates',
            name='kash',
            field=models.TextField(blank=True, null=True, verbose_name='Кэш для построения маршрута'),
        ),
        migrations.AddField(
            model_name='routecoordinates',
            name='transport',
            field=models.CharField(max_length=40, null=True, verbose_name='Вид транспорта'),
        ),
    ]
