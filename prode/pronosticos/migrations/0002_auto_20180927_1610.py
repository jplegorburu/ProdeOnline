# Generated by Django 2.1.1 on 2018-09-27 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pronosticos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partido',
            name='fecha',
            field=models.DateTimeField(),
        ),
    ]
