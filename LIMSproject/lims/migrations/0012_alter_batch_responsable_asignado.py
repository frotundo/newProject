# Generated by Django 4.1.4 on 2023-03-10 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lims', '0011_alter_envase_material_alter_envase_preservante_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='responsable_asignado',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]