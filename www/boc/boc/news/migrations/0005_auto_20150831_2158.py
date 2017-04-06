# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_auto_20150831_2152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 31, 21, 58, 45, 245555), null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='date_updated',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 31, 21, 58, 45, 245635), null=True, blank=True),
        ),
    ]
