# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('statistics', '0002_statisticscontent'),
    ]

    operations = [
        migrations.AddField(
            model_name='statistic',
            name='fund',
            field=models.DecimalField(null=True, max_digits=20, decimal_places=2, blank=True),
            preserve_default=True,
        ),
    ]
