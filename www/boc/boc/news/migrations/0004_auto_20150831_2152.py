# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_auto_20150811_1749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 31, 21, 52, 17, 756397), null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='date_updated',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 31, 21, 52, 17, 756474), null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=True, populate_from=b'title'),
        ),
    ]
