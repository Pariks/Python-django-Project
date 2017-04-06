# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mma', '0009_auto_20150511_0134'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='slug',
            field=autoslug.fields.AutoSlugField(default=None, editable=True, populate_from=b'name'),
            preserve_default=False,
        ),
    ]
