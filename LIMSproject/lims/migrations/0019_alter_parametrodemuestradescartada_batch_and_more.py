# Generated by Django 4.1.4 on 2023-02-13 13:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lims', '0018_rename_dropped_parametrodemuestradescartada_discarded_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parametrodemuestradescartada',
            name='batch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='lims.batch'),
        ),
        migrations.AlterField(
            model_name='parametrodemuestradescartada',
            name='parametro',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lims.parametroespecifico'),
        ),
        migrations.AlterField(
            model_name='parametrodemuestradescartada',
            name='responsable_de_analisis',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='parametrodemuestradescartada',
            name='servicio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lims.servicio'),
        ),
    ]
