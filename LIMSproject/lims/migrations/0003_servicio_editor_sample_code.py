# Generated by Django 4.1.4 on 2023-01-16 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lims', '0002_servicio_observacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicio',
            name='editor_sample_code',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]