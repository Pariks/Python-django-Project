# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0003_auto_20150102_1947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userextrainfo',
            name='phone_number',
            field=models.BigIntegerField(max_length=100),
            preserve_default=True,
        ),
    ]
