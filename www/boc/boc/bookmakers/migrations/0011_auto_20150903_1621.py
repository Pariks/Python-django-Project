# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('bookmakers', '0010_auto_20150831_1823'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='platform',
            field=models.CharField(default='DE', max_length=2, choices=[(b'WI', b'Wide'), (b'TA', b'Tall'), (b'SQ', b'Square')]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bookmaker',
            name='content',
            field=tinymce.models.HTMLField(blank=True),
        ),
    ]
