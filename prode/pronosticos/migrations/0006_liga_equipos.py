# Generated by Django 2.1.1 on 2018-09-28 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pronosticos', '0005_fechaliga'),
    ]

    operations = [
        migrations.AddField(
            model_name='liga',
            name='equipos',
            field=models.ManyToManyField(through='pronosticos.EquipoLiga', to='pronosticos.Equipo'),
        ),
    ]
