# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('investor', '0003_investor_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='investor',
            name='amount',
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
    ]
