# Generated by Django 4.1.4 on 2023-01-13 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lims', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='parametrodemuestra',
            name='peso_final',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='parametrodemuestra',
            name='peso_inicial',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
