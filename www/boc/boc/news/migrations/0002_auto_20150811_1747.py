# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='preview_content',
            field=models.CharField(default=None, max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='article',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 11, 17, 47, 22, 612414), null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='date_updated',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 11, 17, 47, 22, 612473), null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='slug',
            field=models.SlugField(unique=True, blank=True),
        ),
    ]
