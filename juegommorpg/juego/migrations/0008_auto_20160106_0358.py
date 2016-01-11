# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('juego', '0007_auto_20160106_0307'),
    ]

    operations = [
        migrations.CreateModel(
            name='Army',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
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
                ('player', models.ForeignKey(to='juego.Player')),
            ],
        ),
        migrations.CreateModel(
            name='Barrack',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level_build', models.IntegerField()),
                ('player', models.ForeignKey(to='juego.Player')),
            ],
        ),
        migrations.CreateModel(
            name='Deposit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level_build', models.IntegerField()),
                ('capacity', models.IntegerField()),
                ('player', models.ForeignKey(to='juego.Player')),
            ],
        ),
        migrations.CreateModel(
            name='Farm',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level_build', models.IntegerField()),
                ('capacity', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('material', models.CharField(max_length=100)),
                ('player', models.ForeignKey(to='juego.Player')),
            ],
        ),
        migrations.CreateModel(
            name='Intendency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level_build', models.IntegerField()),
                ('player', models.ForeignKey(to='juego.Player')),
            ],
        ),
        migrations.CreateModel(
            name='Mine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level_build', models.IntegerField()),
                ('capacity', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('material', models.CharField(max_length=100)),
                ('production_hour', models.IntegerField()),
                ('player', models.ForeignKey(to='juego.Player')),
            ],
        ),
        migrations.CreateModel(
            name='Wall',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level_build', models.IntegerField()),
                ('defence', models.IntegerField()),
                ('player', models.ForeignKey(to='juego.Player')),
            ],
        ),
        migrations.AlterField(
            model_name='sawmill',
            name='material',
            field=models.CharField(max_length=100),
        ),
    ]
