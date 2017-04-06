# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import tinymce.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('mma', '0004_auto_20150129_0731'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to=b'uploads/news', blank=True)),
                ('content', tinymce.models.HTMLField(blank=True)),
                ('published', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(default=datetime.datetime(2015, 4, 16, 3, 3, 58, 354632), null=True, blank=True)),
                ('date_published', models.DateTimeField(null=True, blank=True)),
                ('date_updated', models.DateTimeField(default=datetime.datetime(2015, 4, 16, 3, 3, 58, 354691), null=True, blank=True)),
                ('slug', models.SlugField(unique=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('event', models.ForeignKey(blank=True, to='mma.Event', null=True)),
                ('fight', models.ForeignKey(blank=True, to='mma.Fight', null=True)),
                ('fighter', models.ForeignKey(blank=True, to='mma.Fighter', null=True)),
                ('promotion', models.ForeignKey(blank=True, to='mma.Promotion', null=True)),
                ('sport', models.ForeignKey(blank=True, to='mma.Sport', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
