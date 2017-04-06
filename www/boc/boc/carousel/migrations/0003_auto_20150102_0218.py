# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carousel', '0002_carouselitem_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carouselitem',
            name='image',
            field=models.ImageField(upload_to=b'media/carousel/', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='carouselitem',
            name='video_url',
            field=models.CharField(max_length=200, blank=True),
            preserve_default=True,
        ),
    ]
