# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('advisory', '0003_auto_20160626_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advisoryboard',
            name='image',
            field=models.ImageField(upload_to=b'media/carousel/', blank=True),
        ),
    ]
