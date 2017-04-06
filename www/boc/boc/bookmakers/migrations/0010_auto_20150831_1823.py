# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('bookmakers', '0009_bookmaker_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmaker',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=True, populate_from=b'name'),
        ),
    ]
