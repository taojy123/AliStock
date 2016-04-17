# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pid', models.CharField(max_length=255, null=True, blank=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('color', models.CharField(max_length=255, null=True, blank=True)),
                ('size', models.CharField(max_length=255, null=True, blank=True)),
                ('pattern', models.CharField(max_length=255, null=True, blank=True)),
                ('url', models.CharField(max_length=255, null=True, blank=True)),
                ('pic', models.ImageField(null=True, upload_to=b'product_pic')),
                ('price', models.FloatField(default=0, null=True, blank=True)),
                ('stock', models.IntegerField(default=0)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('extra', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.IntegerField(default=1)),
                ('price', models.FloatField(default=0, null=True, blank=True)),
                ('comment', models.CharField(max_length=255, null=True, blank=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('extra', models.TextField(null=True, blank=True)),
                ('product', models.ForeignKey(to='alistock.Product')),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.IntegerField(default=1)),
                ('price', models.FloatField(default=0, null=True, blank=True)),
                ('comment', models.CharField(max_length=255, null=True, blank=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('extra', models.TextField(null=True, blank=True)),
                ('product', models.ForeignKey(to='alistock.Product')),
            ],
        ),
    ]
