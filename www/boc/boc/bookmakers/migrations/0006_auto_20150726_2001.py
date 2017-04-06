# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('bookmakers', '0005_auto_20150725_1712'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('size', models.CharField(max_length=2, choices=[(b'WI', b'Wide'), (b'TA', b'Tall'), (b'SQ', b'Square')])),
                ('name', models.CharField(max_length=50)),
                ('banner_html', tinymce.models.HTMLField()),
                ('bookmaker', models.ForeignKey(to='bookmakers.Bookmaker')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='bookmaker',
            name='banner_square',
        ),
        migrations.RemoveField(
            model_name='bookmaker',
            name='banner_tall',
        ),
        migrations.RemoveField(
            model_name='bookmaker',
            name='banner_wide',
        ),
    ]
