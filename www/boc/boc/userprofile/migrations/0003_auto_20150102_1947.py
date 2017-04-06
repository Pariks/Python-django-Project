# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0002_auto_20141231_0328'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userextrainfo',
            name='premium',
        ),
        migrations.RemoveField(
            model_name='userextrainfo',
            name='stripeData',
        ),
    ]
