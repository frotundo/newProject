# Generated by Django 4.1.4 on 2023-03-08 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lims', '0003_servicio_representante_legal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicio',
            name='norma_de_referencia',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
    ]