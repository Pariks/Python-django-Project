# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('predictions', '0004_auto_20150129_0720'),
    ]

    operations = [
        migrations.AddField(
            model_name='prediction',
            name='result',
            field=models.CharField(default=b'Pending', max_length=7, choices=[(b'Win', b'Win'), (b'Loss', b'Loss'), (b'Push', b'Push'), (b'Pending', b'Pending')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='prediction',
            name='bet_type',
            field=models.CharField(max_length=2, choices=[(b'ST', b'Straight Bet'), (b'PA', b'Parlay'), (b'PR', b'Prop')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='predictionarticle',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 10, 3, 49, 47, 894864), null=True, blank=True),
            preserve_default=True,
        ),
    ]
