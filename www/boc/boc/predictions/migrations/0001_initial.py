# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('mma', '0003_event_broadcast'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prediction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fighter1_odds', models.IntegerField(null=True, blank=True)),
                ('fighter2_odds', models.IntegerField(null=True, blank=True)),
                ('fighter1_percent', models.DecimalField(null=True, max_digits=5, decimal_places=2, blank=True)),
                ('fighter2_percent', models.DecimalField(null=True, max_digits=5, decimal_places=2, blank=True)),
                ('bet_type', models.CharField(blank=True, max_length=2, choices=[(b'ST', b'Straight Bet'), (b'PA', b'Parlay')])),
                ('prediction', tinymce.models.HTMLField(null=True, blank=True)),
                ('odds', models.CharField(max_length=20)),
                ('risk', models.DecimalField(max_digits=20, decimal_places=2)),
                ('win', models.DecimalField(max_digits=20, decimal_places=2)),
                ('breakdown', tinymce.models.HTMLField(null=True, blank=True)),
                ('outcome', tinymce.models.HTMLField(null=True, blank=True)),
                ('fight', models.ManyToManyField(to='mma.Fight', null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PredictionArticle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to=b'uploads/predictions', blank=True)),
                ('content', tinymce.models.HTMLField(blank=True)),
                ('timestamp', models.DateTimeField(default=datetime.datetime(2015, 1, 18, 5, 40, 54, 785629), null=True, blank=True)),
                ('open', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='prediction',
            name='prediction_article',
            field=models.ForeignKey(to='predictions.PredictionArticle'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='prediction',
            name='sport',
            field=models.ManyToManyField(to='mma.Sport'),
            preserve_default=True,
        ),
    ]
