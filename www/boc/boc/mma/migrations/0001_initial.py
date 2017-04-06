# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('venue', models.CharField(max_length=50, blank=True)),
                ('city', models.CharField(max_length=50, blank=True)),
            ],
            options={
                'ordering': ['-date'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Fight',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField(blank=True)),
                ('fight_type', models.CharField(blank=True, max_length=2, choices=[(b'ME', b'Main Event'), (b'CO', b'Co-Main Event'), (b'MC', b'Main Card'), (b'PL', b'Preliminary Card')])),
                ('method_of_victory_1', models.CharField(max_length=50, blank=True)),
                ('method_of_victory_2', models.CharField(max_length=50, blank=True)),
                ('round', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('duration', models.CharField(max_length=5, blank=True)),
                ('event', models.ForeignKey(blank=True, to='mma.Event', null=True)),
            ],
            options={
                'ordering': ['order'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Fighter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=40)),
                ('last_name', models.CharField(max_length=40)),
            ],
            options={
                'ordering': ['last_name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WeightClass',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('weight_class', models.CharField(max_length=20, blank=True)),
                ('weight', models.IntegerField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='promotion',
            name='sport',
            field=models.ForeignKey(to='mma.Sport'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fight',
            name='fighter1',
            field=models.ForeignKey(related_name='fighter1', to='mma.Fighter'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fight',
            name='fighter2',
            field=models.ForeignKey(related_name='fighter2', to='mma.Fighter'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fight',
            name='fighter_winner',
            field=models.ForeignKey(related_name='winner', blank=True, to='mma.Fighter', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fight',
            name='weight_class',
            field=models.ForeignKey(blank=True, to='mma.WeightClass', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='promotion',
            field=models.ForeignKey(to='mma.Promotion'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='sport',
            field=models.ForeignKey(to='mma.Sport'),
            preserve_default=True,
        ),
    ]
