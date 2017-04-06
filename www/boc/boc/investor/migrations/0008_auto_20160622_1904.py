# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('investor', '0007_auto_20160622_1415'),
    ]

    operations = [
        migrations.RenameField(
            model_name='investorrelation',
            old_name='text',
            new_name='content',
        ),
    ]
