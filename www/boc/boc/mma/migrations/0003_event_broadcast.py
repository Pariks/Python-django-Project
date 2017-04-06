# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mma', '0002_event_poster'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='broadcast',
            field=models.CharField(default=None, max_length=25, blank=True),
            preserve_default=False,
        ),
    ]
