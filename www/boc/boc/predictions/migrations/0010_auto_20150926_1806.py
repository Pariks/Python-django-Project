# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('predictions', '0009_auto_20150831_2242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prediction',
            name='result',
            field=models.CharField(default=b'Pending', max_length=7, choices=[(b'Win', b'Win'), (b'Loss', b'Loss'), (b'Push', b'Push'), (b'Pending', b'Pending'), (b'Void', b'Void')]),
        ),
    ]
