# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('juego', '0008_auto_20160106_0358'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event_atack',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.IntegerField()),
                ('procesed', models.IntegerField()),
                ('unit1', models.IntegerField()),
                ('unit2', models.IntegerField()),
                ('unit3', models.IntegerField()),
                ('unit4', models.IntegerField()),
                ('unit5', models.IntegerField()),
                ('unit6', models.IntegerField()),
                ('unit7', models.IntegerField()),
                ('unit8', models.IntegerField()),
                ('unit9', models.IntegerField()),
                ('unit10', models.IntegerField()),
                ('unit99', models.IntegerField()),
                ('back_time', models.IntegerField()),
                ('wood', models.IntegerField()),
                ('iron', models.IntegerField()),
                ('player', models.ForeignKey(related_name='player_atack', to='juego.Player')),
                ('player_victim', models.ForeignKey(related_name='player_victim_atack', to='juego.Player')),
            ],
        ),
        migrations.CreateModel(
            name='Event_create',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.IntegerField()),
                ('procesed', models.IntegerField()),
                ('creature', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('player', models.ForeignKey(to='juego.Player')),
            ],
        ),
        migrations.CreateModel(
            name='Event_trade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.IntegerField()),
                ('procesed', models.IntegerField()),
                ('wood', models.IntegerField()),
                ('iron', models.IntegerField()),
                ('workers', models.IntegerField()),
                ('back_time', models.IntegerField()),
                ('player', models.ForeignKey(related_name='player_trade', to='juego.Player')),
                ('player_victim', models.ForeignKey(related_name='player_victim_trade', to='juego.Player')),
            ],
        ),
        migrations.CreateModel(
            name='Event_update',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.IntegerField()),
                ('procesed', models.IntegerField()),
                ('build', models.CharField(max_length=100)),
                ('player', models.ForeignKey(to='juego.Player')),
            ],
        ),
    ]
