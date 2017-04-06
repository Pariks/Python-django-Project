# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0011_auto_20150923_0423'),
    ]

    operations = [
        migrations.AddField(
            model_name='userextrainfo',
            name='news_letter',
            field=models.BooleanField(default=True),
        ),
    ]
