# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookmakers', '0004_auto_20150725_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmaker',
            name='affiliate_url',
            field=models.CharField(max_length=100, blank=True, null=True),
            preserve_default=True,
        ),
    ]
