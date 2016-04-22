# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alistock', '0002_product_special'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='is_special',
            field=models.BooleanField(default=False),
        ),
    ]
