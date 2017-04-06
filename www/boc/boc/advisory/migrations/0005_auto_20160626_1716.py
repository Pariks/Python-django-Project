# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('advisory', '0004_auto_20160626_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advisoryboard',
            name='image',
            field=models.ImageField(upload_to=b'media/advisory/', blank=True),
        ),
    ]
