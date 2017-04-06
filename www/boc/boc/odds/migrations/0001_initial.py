# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bookmakers', '0002_bookmaker_api_id'),
        ('mma', '0009_auto_20150511_0134'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bet1', models.CharField(max_length=200)),
                ('bet2', models.CharField(max_length=200, null=True, blank=True)),
                ('odds1', models.DecimalField(null=True, max_digits=8, decimal_places=3, blank=True)),
                ('odds2', models.DecimalField(null=True, max_digits=8, decimal_places=3, blank=True)),
                ('odds1_open', models.DecimalField(null=True, max_digits=8, decimal_places=3, blank=True)),
                ('odds2_open', models.DecimalField(null=True, max_digits=8, decimal_places=3, blank=True)),
                ('fighter1_name', models.CharField(max_length=80, null=True, blank=True)),
                ('fighter2_name', models.CharField(max_length=80, null=True, blank=True)),
                ('event_date', models.DateField(null=True, blank=True)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BetType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fighter_no', models.IntegerField(choices=[(0, 0), (1, 1), (2, 2)])),
                ('bet_type_id', models.CharField(max_length=20)),
                ('category', models.CharField(max_length=50)),
                ('bet1_name', models.CharField(max_length=100, blank=True)),
                ('bet2_name', models.CharField(max_length=100, blank=True)),
                ('match_text', models.CharField(max_length=500, blank=True)),
                ('value', models.DecimalField(null=True, max_digits=3, decimal_places=1, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Odds',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('odds1', models.DecimalField(null=True, max_digits=8, decimal_places=3, blank=True)),
                ('odds2', models.DecimalField(null=True, max_digits=8, decimal_places=3, blank=True)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('bet', models.ForeignKey(related_name='odds', to='odds.Bet')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='bet',
            name='bet_type',
            field=models.ForeignKey(blank=True, to='odds.BetType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bet',
            name='event',
            field=models.ForeignKey(blank=True, to='mma.Event', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bet',
            name='fight',
            field=models.ForeignKey(related_name='bet', blank=True, to='mma.Fight', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bet',
            name='fighter1',
            field=models.ForeignKey(related_name='bet_fighter1', blank=True, to='mma.Fighter', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bet',
            name='fighter2',
            field=models.ForeignKey(related_name='bet_fighter2', blank=True, to='mma.Fighter', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bet',
            name='sportsbook',
            field=models.ForeignKey(to='bookmakers.Bookmaker'),
            preserve_default=True,
        ),
    ]
