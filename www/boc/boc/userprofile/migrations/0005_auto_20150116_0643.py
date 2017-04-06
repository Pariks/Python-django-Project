# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0004_auto_20150102_1953'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userextrainfo',
            name='address',
        ),
        migrations.RemoveField(
            model_name='userextrainfo',
            name='city',
        ),
        migrations.RemoveField(
            model_name='userextrainfo',
            name='city_of_birth',
        ),
        migrations.RemoveField(
            model_name='userextrainfo',
            name='date_of_birth',
        ),
        migrations.RemoveField(
            model_name='userextrainfo',
            name='mothers_maiden_name',
        ),
        migrations.RemoveField(
            model_name='userextrainfo',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='userextrainfo',
            name='postal_code',
        ),
        migrations.RemoveField(
            model_name='userextrainfo',
            name='province',
        ),
    ]
