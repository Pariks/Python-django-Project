# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('bookmakers', '0003_bookmaker_banner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookmaker',
            name='banner',
        ),
        migrations.AddField(
            model_name='bookmaker',
            name='affiliate_url',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bookmaker',
            name='banner_square',
            field=tinymce.models.HTMLField(blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bookmaker',
            name='banner_tall',
            field=tinymce.models.HTMLField(blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bookmaker',
            name='banner_wide',
            field=tinymce.models.HTMLField(blank=True),
            preserve_default=True,
        ),
    ]
