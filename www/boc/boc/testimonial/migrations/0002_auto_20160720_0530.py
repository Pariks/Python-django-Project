# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testimonial', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='testimonialitem',
            options={'ordering': ['-order']},
        ),
        migrations.AddField(
            model_name='testimonialitem',
            name='video',
            field=models.FileField(null=True, upload_to=b'', blank=True),
        ),
    ]
