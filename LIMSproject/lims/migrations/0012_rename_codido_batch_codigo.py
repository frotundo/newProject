# Generated by Django 4.1.4 on 2023-02-09 12:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lims', '0011_batch_alter_parametrodemuestra_created_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='batch',
            old_name='codido',
            new_name='codigo',
        ),
    ]
