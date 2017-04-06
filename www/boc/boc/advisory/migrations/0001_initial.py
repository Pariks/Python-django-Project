# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdvisoryBoard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.TextField(blank=True)),
                ('content', tinymce.models.HTMLField()),
                ('image', models.ImageField(upload_to=b'media/advisory/', blank=True)),
                ('order', models.IntegerField()),
            ],
        ),
    ]
