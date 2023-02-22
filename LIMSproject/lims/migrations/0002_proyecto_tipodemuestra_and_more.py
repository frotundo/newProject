# Generated by Django 4.1.4 on 2023-02-22 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lims', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='proyecto',
            name='TipoDeMuestra',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='parametrodemuestra',
            name='analisis_externos',
            field=models.BooleanField(default=False),
        ),
    ]
