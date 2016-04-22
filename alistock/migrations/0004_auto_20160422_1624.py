# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alistock', '0003_sale_is_special'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='special',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='price',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='sale',
            name='price',
            field=models.FloatField(default=0),
        ),
    ]
