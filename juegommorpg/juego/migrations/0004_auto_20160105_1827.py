# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('juego', '0003_auto_20151102_2305'),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('faction', models.CharField(max_length=100)),
                ('town', models.CharField(max_length=100)),
                ('world', models.IntegerField()),
                ('coordinateX', models.IntegerField()),
                ('coordinateY', models.IntegerField()),
                ('lastlogin', models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
