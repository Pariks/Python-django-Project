# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carousel', '0008_carouselitem_show_or_hide_button'),
    ]

    operations = [
        migrations.CreateModel(
            name='FundsUnderManagement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.FloatField()),
            ],
        ),
    ]
