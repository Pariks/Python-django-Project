# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('odds', '0002_auto_20150511_0554'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bet',
            name='fighter1_name',
        ),
        migrations.RemoveField(
            model_name='bet',
            name='fighter2_name',
        ),
    ]
