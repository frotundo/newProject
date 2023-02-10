# Generated by Django 4.1.4 on 2023-02-09 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lims', '0012_rename_codido_batch_codigo'),
    ]

    operations = [
        migrations.AddField(
            model_name='batch',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='batch',
            name='creator_user',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
