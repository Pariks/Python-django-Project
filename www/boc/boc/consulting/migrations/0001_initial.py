# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Benefit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', tinymce.models.HTMLField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ScheduleConsultation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=300)),
                ('matter', models.TextField()),
                ('date', models.DateField()),
                ('start_time_1', models.TimeField()),
                ('start_time_2', models.TimeField()),
                ('start_time_3', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='SubscriptionInfo',
            fields=[
                ('duration', models.CharField(max_length=1, unique=True, serialize=False, primary_key=True, choices=[(b'W', b'weekly'), (b'M', b'monthly'), (b'Y', b'annually')])),
                ('price', models.DecimalField(max_digits=25, decimal_places=2)),
            ],
        ),
        migrations.AddField(
            model_name='benefit',
            name='subscriptonType',
            field=models.ForeignKey(default=b'', to='consulting.SubscriptionInfo'),
        ),
    ]
