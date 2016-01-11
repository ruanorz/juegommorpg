# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('juego', '0005_auto_20160106_0213'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sawmill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level_build', models.IntegerField()),
                ('capacity', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('material', models.IntegerField()),
                ('production_hour', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='player',
            name='email',
            field=models.CharField(unique=True, max_length=100),
        ),
        migrations.AddField(
            model_name='sawmill',
            name='id_player',
            field=models.ForeignKey(to='juego.Player'),
        ),
    ]
