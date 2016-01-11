# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('juego', '0010_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report_battle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(max_length=500)),
                ('date', models.CharField(max_length=100)),
                ('time', models.IntegerField()),
                ('victory', models.IntegerField()),
                ('player', models.ForeignKey(to='juego.Player')),
            ],
        ),
        migrations.CreateModel(
            name='Report_trade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(max_length=500)),
                ('date', models.CharField(max_length=100)),
                ('time', models.IntegerField()),
                ('victory', models.IntegerField()),
                ('player', models.ForeignKey(to='juego.Player')),
            ],
        ),
    ]
