# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0006_auto_20150831_2241'),
        ('followpost', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FollowPostItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField()),
                ('date_commented', models.DateTimeField(auto_now_add=True)),
                ('child', models.IntegerField(default=1)),
                ('article', models.ForeignKey(to='news.Article')),
                ('comment_replies', models.ForeignKey(to='followpost.FollowPostItem', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
