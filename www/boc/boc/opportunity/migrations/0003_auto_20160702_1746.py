# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('opportunity', '0002_auto_20160702_1731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opportunityitem',
            name='content',
            field=tinymce.models.HTMLField(),
        ),
    ]
