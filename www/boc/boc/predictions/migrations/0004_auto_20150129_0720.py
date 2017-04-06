# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('predictions', '0003_auto_20150126_0215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='predictionarticle',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 29, 7, 20, 43, 364536), null=True, blank=True),
            preserve_default=True,
        ),
    ]
