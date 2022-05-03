# Generated by Django 4.0.1 on 2022-03-15 17:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0011_startloc_endlat_startloc_endlong_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Places',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('places_long', models.FloatField(blank=True, null=True, verbose_name='Долгота места')),
                ('places_lat', models.FloatField(blank=True, null=True, verbose_name='Широта места')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='places', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]