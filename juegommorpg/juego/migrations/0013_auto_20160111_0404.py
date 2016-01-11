# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('juego', '0012_remove_report_trade_victory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='email',
            field=models.CharField(max_length=100),
        ),
    ]
