# Generated by Django 4.0.1 on 2022-03-17 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_routecoordinates_delete_startloc'),
    ]

    operations = [
        migrations.AddField(
            model_name='places',
            name='name',
            field=models.TextField(blank=True, null=True, verbose_name='Название места'),
        ),
    ]
