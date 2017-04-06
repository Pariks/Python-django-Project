# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mma', '0003_event_broadcast'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fight',
            name='order',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
