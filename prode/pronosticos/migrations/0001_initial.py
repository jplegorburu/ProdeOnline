# Generated by Django 2.1.1 on 2018-09-27 14:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Equipo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='EquipoLiga',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('equipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='equipo', to='pronosticos.Equipo')),
            ],
            options={
                'ordering': ('liga',),
            },
        ),
        migrations.CreateModel(
            name='Liga',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('tipo', models.CharField(choices=[('temporada', 'Temporada'), ('copa', 'Copa')], default='temporada', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Partido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('local_gol', models.IntegerField()),
                ('visita_gol', models.IntegerField()),
                ('fecha', models.DateField()),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente'), ('jugando', 'Jugando'), ('suspendido', 'Suspendido'), ('finalizado', 'Finalizado')], default='pendiente', max_length=11)),
                ('liga', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liga_partido', to='pronosticos.Liga')),
                ('local', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='equipo_local', to='pronosticos.Equipo')),
                ('visita', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='equipo_visita', to='pronosticos.Equipo')),
            ],
        ),
        migrations.AddField(
            model_name='equipoliga',
            name='liga',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liga', to='pronosticos.Liga'),
        ),
    ]