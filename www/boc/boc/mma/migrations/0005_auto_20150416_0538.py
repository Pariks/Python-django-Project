# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mma', '0004_auto_20150129_0731'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='api_id',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fight',
            name='api_id',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fighter',
            name='api_id',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='promotion',
            name='api_id',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='weightclass',
            name='api_id',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
