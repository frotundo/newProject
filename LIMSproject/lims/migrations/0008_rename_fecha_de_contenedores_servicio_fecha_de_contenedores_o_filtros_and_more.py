# Generated by Django 4.1.4 on 2023-02-27 12:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lims', '0007_filtro'),
    ]

    operations = [
        migrations.RenameField(
            model_name='servicio',
            old_name='fecha_de_contenedores',
            new_name='fecha_de_contenedores_o_filtros',
        ),
        migrations.AddField(
            model_name='servicio',
            name='filtros',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='lims.filtro'),
        ),
        migrations.CreateModel(
            name='ModeloDeServicioDeFiltro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_modelo', models.CharField(max_length=200, unique=True)),
                ('cliente', models.CharField(max_length=5)),
                ('area', models.CharField(blank=True, max_length=200, null=True)),
                ('punto_de_muestreo', models.CharField(max_length=200)),
                ('tipo_de_muestra', models.CharField(max_length=200)),
                ('observacion', models.TextField(blank=True, null=True)),
                ('fecha_de_entrega_cliente', models.DateField(blank=True, null=True)),
                ('norma_de_referencia', models.CharField(max_length=254)),
                ('responsable', models.CharField(max_length=200)),
                ('rCA', models.CharField(max_length=254)),
                ('etfa', models.BooleanField()),
                ('muestreado_por_algoritmo', models.CharField(max_length=254)),
                ('created', models.DateTimeField()),
                ('creator_user', models.CharField(max_length=100)),
                ('filtro', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='lims.filtro')),
                ('proyecto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='lims.proyecto')),
            ],
        ),
        migrations.AddField(
            model_name='servicio',
            name='modelo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='lims.modelodeserviciodefiltro'),
        ),
    ]
