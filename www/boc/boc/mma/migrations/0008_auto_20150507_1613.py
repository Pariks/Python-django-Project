# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mma', '0007_weightclass_sport'),
    ]

    operations = [
        migrations.AddField(
            model_name='fight',
            name='is_cancelled',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fight',
            name='is_championship',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
