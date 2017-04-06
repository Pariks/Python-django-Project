# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_auto_20150811_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 11, 17, 49, 18, 95704), null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='date_updated',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 11, 17, 49, 18, 95767), null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='preview_content',
            field=models.TextField(blank=True),
        ),
    ]
