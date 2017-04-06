# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookmakers', '0011_auto_20150903_1621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='platform',
            field=models.CharField(max_length=2, choices=[(b'DE', b'Desktop'), (b'MO', b'Mobile')]),
        ),
    ]
