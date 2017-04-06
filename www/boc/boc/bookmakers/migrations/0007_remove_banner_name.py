# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookmakers', '0006_auto_20150726_2001'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='banner',
            name='name',
        ),
    ]
