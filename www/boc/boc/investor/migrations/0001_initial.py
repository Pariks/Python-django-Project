# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('locality', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Investor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_of_birth', models.DateField()),
                ('phone_number', models.BigIntegerField(max_length=15)),
                ('address', models.CharField(max_length=100)),
                ('postal_code', models.CharField(max_length=6, blank=True)),
                ('city', models.CharField(max_length=50)),
                ('country', models.ForeignKey(to='locality.Country')),
                ('territory', models.ForeignKey(blank=True, to='locality.Territory', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
