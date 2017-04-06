# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookmakers', '0002_bookmaker_api_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookmaker',
            name='banner',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
    ]
