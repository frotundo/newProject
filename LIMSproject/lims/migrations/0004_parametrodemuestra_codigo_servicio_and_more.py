# Generated by Django 4.1.4 on 2023-01-11 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lims', '0003_alter_parametrodemuestra_parametro'),
    ]

    operations = [
        migrations.AddField(
            model_name='parametrodemuestra',
            name='codigo_servicio',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='servicio',
            name='fecha_de_muestreo',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='servicio',
            name='fecha_de_recepción',
            field=models.DateField(blank=True, null=True),
        ),
    ]