# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mma', '0006_auto_20150426_0530'),
    ]

    operations = [
        migrations.AddField(
            model_name='weightclass',
            name='sport',
            field=models.ForeignKey(blank=True, to='mma.Sport', null=True),
            preserve_default=True,
        ),
    ]
