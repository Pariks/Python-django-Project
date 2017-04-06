# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_auto_20150831_2235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatmessage',
            name='text',
            field=models.TextField(),
        ),
    ]
