# Generated by Django 4.1.4 on 2023-03-08 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lims', '0004_alter_servicio_norma_de_referencia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicio',
            name='rCA',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
    ]