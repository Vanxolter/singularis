# Generated by Django 4.0.1 on 2022-03-08 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_airports_airid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='airports',
            name='airid',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='airports id'),
        ),
    ]