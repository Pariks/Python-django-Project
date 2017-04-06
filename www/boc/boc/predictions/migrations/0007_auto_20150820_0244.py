# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('predictions', '0006_auto_20150709_1630'),
    ]

    operations = [
        migrations.AddField(
            model_name='prediction',
            name='order',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='predictionarticle',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 20, 2, 44, 9, 581399), null=True, blank=True),
        ),
    ]
