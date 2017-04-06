# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('predictions', '0007_auto_20150820_0244'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='prediction',
            options={'ordering': ['-prediction_article__timestamp', 'order']},
        ),
        migrations.AddField(
            model_name='predictionarticle',
            name='slug',
            field=autoslug.fields.AutoSlugField(default=None, editable=True, populate_from=b'title'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='predictionarticle',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 31, 21, 57, 34, 518384), null=True, blank=True),
        ),
    ]
