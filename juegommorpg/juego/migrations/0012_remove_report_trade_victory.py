# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('juego', '0011_report_battle_report_trade'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report_trade',
            name='victory',
        ),
    ]
