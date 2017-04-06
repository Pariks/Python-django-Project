# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('investor', '0002_auto_20150410_1615'),
    ]

    operations = [
        migrations.AddField(
            model_name='investor',
            name='approved',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
