# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('odds', '0007_delete_oddstable'),
    ]

    operations = [
        migrations.CreateModel(
            name='OddsTable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('odds_table', models.TextField()),
            ],
        ),
    ]
