# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('predictions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prediction',
            name='bet_type',
            field=models.CharField(max_length=2, choices=[(b'ST', b'Straight Bet'), (b'PA', b'Parlay')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='predictionarticle',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 25, 17, 22, 27, 87496), null=True, blank=True),
            preserve_default=True,
        ),
    ]
