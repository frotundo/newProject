# Generated by Django 4.1.4 on 2023-03-09 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lims', '0007_proyecto_norma_de_referencia_proyecto_rca_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proyecto',
            name='parametros_externos',
        ),
        migrations.AlterField(
            model_name='modelodeserviciodefiltro',
            name='etfa',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='etfa',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
