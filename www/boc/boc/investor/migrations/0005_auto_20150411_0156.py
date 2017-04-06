# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('investor', '0004_investor_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='investor',
            name='cell_number',
            field=models.CharField(default=None, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='investor',
            name='distribution',
            field=models.CharField(default=None, max_length=2, choices=[(b'RE', b'Reinvest'), (b'CH', b'Cheque')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='investor',
            name='investment_timeframe',
            field=models.CharField(default=None, max_length=2, choices=[(b'12', b'12 Months'), (b'24', b'24 Months'), (b'36', b'36 Months')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='investor',
            name='submission_date',
            field=models.DateTimeField(default=datetime.datetime.now, blank=True),
            preserve_default=True,
        ),
    ]
