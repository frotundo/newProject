# Generated by Django 4.1.4 on 2023-03-09 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lims', '0008_remove_proyecto_parametros_externos_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyecto',
            name='etfa',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]