# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('odds', '0006_oddstable'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OddsTable',
        ),
    ]
