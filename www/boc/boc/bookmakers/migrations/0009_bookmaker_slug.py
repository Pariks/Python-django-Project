# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('bookmakers', '0008_auto_20150829_2155'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookmaker',
            name='slug',
            field=autoslug.fields.AutoSlugField(default=None, populate_from=b'name', editable=False),
            preserve_default=False,
        ),
    ]
