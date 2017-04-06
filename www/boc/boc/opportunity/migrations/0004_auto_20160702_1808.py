# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('opportunity', '0003_auto_20160702_1746'),
    ]

    operations = [
        migrations.AddField(
            model_name='opportunityitem',
            name='title',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='opportunityitem',
            name='content',
            field=tinymce.models.HTMLField(blank=True),
        ),
    ]
