# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carousel', '0004_carouselitem_subtitle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carouselitem',
            name='subtitle',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='carouselitem',
            name='title',
            field=models.TextField(blank=True),
        ),
    ]
