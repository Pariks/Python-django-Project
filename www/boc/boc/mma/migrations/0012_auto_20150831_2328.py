# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
import mma.models


class Migration(migrations.Migration):

    dependencies = [
        ('mma', '0011_auto_20150831_2315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=True, populate_from=mma.models.event_sluggify),
        ),
    ]
