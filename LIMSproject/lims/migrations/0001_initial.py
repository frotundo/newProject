# Generated by Django 4.1.4 on 2022-12-23 13:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titular', models.CharField(max_length=200, unique=True)),
                ('direccion', models.CharField(max_length=200)),
                ('rut', models.CharField(max_length=10, unique=True)),
                ('actividad', models.CharField(max_length=250)),
                ('email', models.EmailField(max_length=254, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='NormaDeReferencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('norma', models.CharField(max_length=254, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='RepresentanteLegalCliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('rut', models.CharField(max_length=200, unique=True)),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lims.cliente')),
            ],
        ),
        migrations.CreateModel(
            name='RCACliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rca_asociada', models.CharField(max_length=200)),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lims.cliente')),
            ],
        ),
        migrations.CreateModel(
            name='PuntoDeMuestreo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200, unique=True)),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lims.cliente')),
            ],
        ),
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_de_Proyecto', models.CharField(max_length=254)),
                ('codigo_de_proyecto', models.CharField(max_length=10)),
                ('servicio_ETFA', models.BooleanField()),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lims.cliente')),
                ('norma_de_referencia', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lims.normadereferencia')),
                ('punto_de_muestreo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lims.puntodemuestreo')),
                ('rCA', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lims.rcacliente')),
            ],
        ),
        migrations.CreateModel(
            name='ContactoCliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('rut', models.CharField(max_length=200, unique=True)),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lims.cliente')),
            ],
        ),
    ]
