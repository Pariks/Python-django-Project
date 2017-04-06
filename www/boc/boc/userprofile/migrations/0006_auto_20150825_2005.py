# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0005_auto_20150116_0643'),
    ]

    operations = [
        migrations.AddField(
            model_name='userextrainfo',
            name='amount',
            field=models.IntegerField(default=10),
        ),
        migrations.AddField(
            model_name='userextrainfo',
            name='chat_sound',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='userextrainfo',
            name='odds_format',
            field=models.CharField(blank=True, max_length=2, choices=[(b'AM', b'American'), (b'DE', b'Decimal'), (b'PR', b'Implied Probability'), (b'RE', b'Return On')]),
        ),
    ]
