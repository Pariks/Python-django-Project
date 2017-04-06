# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('predictions', '0002_auto_20150125_1722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prediction',
            name='fight',
            field=models.ManyToManyField(to='mma.Fight'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='predictionarticle',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 26, 2, 15, 4, 97407), null=True, blank=True),
            preserve_default=True,
        ),
    ]
