# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('bookmakers', '0012_auto_20160607_1955'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookmakerHead',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', tinymce.models.HTMLField(blank=True)),
            ],
        ),
    ]
