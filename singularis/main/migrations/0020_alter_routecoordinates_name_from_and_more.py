# Generated by Django 4.0.1 on 2022-03-24 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_alter_places_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='routecoordinates',
            name='name_from',
            field=models.CharField(max_length=400, null=True, verbose_name='Откуда'),
        ),
        migrations.AlterField(
            model_name='routecoordinates',
            name='name_to',
            field=models.CharField(max_length=400, null=True, verbose_name='Куда'),
        ),
    ]
