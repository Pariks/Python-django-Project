# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookmakers', '0007_remove_banner_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookmaker',
            name='bonus',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AddField(
            model_name='bookmaker',
            name='countries_restricted',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AddField(
            model_name='bookmaker',
            name='founded',
            field=models.CharField(max_length=10, blank=True),
        ),
        migrations.AddField(
            model_name='bookmaker',
            name='known_for',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AddField(
            model_name='bookmaker',
            name='license',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AddField(
            model_name='bookmaker',
            name='website',
            field=models.CharField(max_length=100, blank=True),
        ),
    ]
