# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserExtraInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_of_birth', models.DateField()),
                ('address', models.CharField(max_length=100)),
                ('postal_code', models.CharField(max_length=6)),
                ('city', models.CharField(max_length=50)),
                ('province', models.CharField(max_length=50)),
                ('phone_number', models.IntegerField(max_length=100)),
                ('mothers_maiden_name', models.CharField(max_length=50)),
                ('city_of_birth', models.CharField(max_length=50)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
