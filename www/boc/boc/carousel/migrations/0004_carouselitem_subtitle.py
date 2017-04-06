# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carousel', '0003_auto_20150102_0218'),
    ]

    operations = [
        migrations.AddField(
            model_name='carouselitem',
            name='subtitle',
            field=models.TextField(default=2),
            preserve_default=False,
        ),
    ]
