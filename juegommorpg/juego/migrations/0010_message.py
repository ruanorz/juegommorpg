# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('juego', '0009_event_atack_event_create_event_trade_event_update'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('text', models.TextField(max_length=500)),
                ('read', models.IntegerField()),
                ('date', models.DateField()),
                ('time', models.IntegerField()),
                ('receiver', models.ForeignKey(related_name='player_receiver', to='juego.Player')),
                ('transmitter', models.ForeignKey(related_name='player_transmitter', to='juego.Player')),
            ],
        ),
    ]
