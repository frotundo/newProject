# Generated by Django 4.1.4 on 2023-03-09 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lims', '0009_alter_proyecto_etfa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='actividad',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='direccion',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
