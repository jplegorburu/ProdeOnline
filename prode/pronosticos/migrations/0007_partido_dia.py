# Generated by Django 2.1.1 on 2018-09-28 22:29

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pronosticos', '0006_liga_equipos'),
    ]

    operations = [
        migrations.AddField(
            model_name='partido',
            name='dia',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]