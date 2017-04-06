# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('predictions', '0005_auto_20150210_0349'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='predictionarticle',
            options={'ordering': ['-timestamp']},
        ),
        migrations.AlterField(
            model_name='prediction',
            name='fight',
            field=models.ManyToManyField(to='mma.Fight', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='predictionarticle',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 9, 16, 30, 17, 611044), null=True, blank=True),
            preserve_default=True,
        ),
    ]
