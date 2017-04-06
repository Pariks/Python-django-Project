# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('predictions', '0008_auto_20150831_2157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='predictionarticle',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True, blank=True),
        ),
    ]
