# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alistock', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='special',
            field=models.FloatField(default=0, null=True, blank=True),
        ),
    ]
