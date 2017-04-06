# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('odds', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bet',
            name='odds1_prev',
            field=models.DecimalField(null=True, max_digits=8, decimal_places=3, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bet',
            name='odds2_prev',
            field=models.DecimalField(null=True, max_digits=8, decimal_places=3, blank=True),
            preserve_default=True,
        ),
    ]
