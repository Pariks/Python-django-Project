# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0009_auto_20150912_2055'),
    ]

    operations = [
        migrations.AddField(
            model_name='phonenumber',
            name='sent',
            field=models.BooleanField(default=False),
        ),
    ]
