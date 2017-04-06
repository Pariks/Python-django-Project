# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('odds', '0003_auto_20150517_0246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bet',
            name='odds1',
            field=models.DecimalField(null=True, max_digits=9, decimal_places=4, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bet',
            name='odds1_open',
            field=models.DecimalField(null=True, max_digits=9, decimal_places=4, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bet',
            name='odds1_prev',
            field=models.DecimalField(null=True, max_digits=9, decimal_places=4, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bet',
            name='odds2',
            field=models.DecimalField(null=True, max_digits=9, decimal_places=4, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bet',
            name='odds2_open',
            field=models.DecimalField(null=True, max_digits=9, decimal_places=4, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bet',
            name='odds2_prev',
            field=models.DecimalField(null=True, max_digits=9, decimal_places=4, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='odds',
            name='odds1',
            field=models.DecimalField(null=True, max_digits=9, decimal_places=4, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='odds',
            name='odds2',
            field=models.DecimalField(null=True, max_digits=9, decimal_places=4, blank=True),
            preserve_default=True,
        ),
    ]
