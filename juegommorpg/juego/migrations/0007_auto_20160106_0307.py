# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('juego', '0006_auto_20160106_0258'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sawmill',
            old_name='id_player',
            new_name='player',
        ),
    ]
