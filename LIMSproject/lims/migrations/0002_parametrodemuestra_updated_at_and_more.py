# Generated by Django 4.1.4 on 2023-03-07 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lims', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='parametrodemuestra',
            name='updated_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='parametroespecifico',
            name='updated_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='servicio',
            name='updated_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
