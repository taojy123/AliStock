# -*- coding: utf-8 -*-

from django.db import models


class Product(models.Model):
    pid = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    color = models.CharField(max_length=255, blank=True, null=True)
    size = models.CharField(max_length=255, blank=True, null=True)
    pattern = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    pic = models.ImageField(upload_to='product_pic', null=True)
    price = models.FloatField(default=0, blank=True, null=True)
    stock = models.IntegerField(default=0)
    update_time = models.DateTimeField(auto_now=True)
    extra = models.TextField(blank=True, null=True)


class Purchase(models.Model):
    product = models.ForeignKey(Product)
    quantity = models.IntegerField(default=0)
    price = models.FloatField(default=0, blank=True, null=True)
    comment = models.CharField(max_length=255, blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    extra = models.TextField(blank=True, null=True)


class Sale(models.Model):
    product = models.ForeignKey(Product)
    quantity = models.IntegerField(default=0)
    price = models.FloatField(default=0, blank=True, null=True)
    comment = models.CharField(max_length=255, blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    extra = models.TextField(blank=True, null=True)

