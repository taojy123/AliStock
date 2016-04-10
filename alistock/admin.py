# -*- coding: utf-8 -*-

from django.contrib import admin
from models import *


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'pid', 'name', 'extra', 'update_time')


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity', 'price', 'comment', 'create_time')


class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity', 'price', 'comment', 'create_time')


admin.site.register(Product, ProductAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Sale, SaleAdmin)

