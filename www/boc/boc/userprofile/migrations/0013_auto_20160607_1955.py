# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0012_userextrainfo_news_letter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userextrainfo',
            name='odds_format',
            field=models.CharField(default=b'AM', max_length=2, blank=True, choices=[(b'AM', b'American'), (b'DE', b'Decimal'), (b'PR', b'Implied Probability'), (b'RE', b'Return On')]),
        ),
    ]
