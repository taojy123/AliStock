# -*- coding: utf-8 -*-

import datetime
from django.db import models
from django.db.models import Sum


class Product(models.Model):
    pid = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    color = models.CharField(max_length=255, blank=True, null=True)
    size = models.CharField(max_length=255, blank=True, null=True)
    pattern = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    pic = models.ImageField(upload_to='product_pic', null=True)
    price = models.FloatField(default=0)
    special = models.FloatField(default=0)
    stock = models.IntegerField(default=0)
    update_time = models.DateTimeField(auto_now=True)
    extra = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return u'%s %s %s %s' % (self.name, self.color, self.size, self.pattern)

    @property
    def sale_quantity(self):
        return self.sale_set.all().aggregate(sum=Sum('quantity')).get('sum', 0) or 0

    @property
    def current_price(self):
        return self.special if self.special > 0 else self.price

class Purchase(models.Model):
    product = models.ForeignKey(Product)
    quantity = models.IntegerField(default=1)
    price = models.FloatField(default=0)
    comment = models.CharField(max_length=255, blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    extra = models.TextField(blank=True, null=True)


class Sale(models.Model):
    product = models.ForeignKey(Product)
    quantity = models.IntegerField(default=1)
    price = models.FloatField(default=0)
    comment = models.CharField(max_length=255, blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    extra = models.TextField(blank=True, null=True)
    is_special = models.BooleanField(default=False)

    @property
    def is_today(self):
        now = datetime.datetime.now()
        t = self.create_time
        return now.year == t.year and now.month == t.month and now.day == t.day
