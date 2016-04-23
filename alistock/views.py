# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.contrib.sites.models import Site
from django.conf import settings
from models import *
import datetime
import xlwt
import os
import uuid
import StringIO


def ip_required(func=None):
    def _d(request, *args, **kwargs):

        if request.user.is_staff:
            return func(request, *args, **kwargs)

        allow_ip = Site.objects.filter(domain='allow_ip').first().name
        client_ip = request.META.get('REMOTE_ADDR', '1.1.1.1')
        if client_ip[:-3] in allow_ip:
            return func(request, *args, **kwargs)

        return HttpResponseRedirect(settings.LOGIN_URL)
    return _d


def index(request):
    client_ip = request.META.get('REMOTE_ADDR', '1.1.1.1')
    return render_to_response('index.html', locals())


# ======== Product =====================

@login_required()
def product_list(request):
    products = Product.objects.order_by('-update_time')

    for product in products:
        purchase_sum = product.purchase_set.all().aggregate(sum=Sum('quantity')).get('sum', 0) or 0
        sale_sum = product.sale_set.all().aggregate(sum=Sum('quantity')).get('sum', 0) or 0
        stock = purchase_sum - sale_sum
        if stock != product.stock:
            product.stock = stock
            product.save()

    return render_to_response('product_list.html', locals())


@login_required()
def product_add(request):
    pid = request.POST.get("pid")
    name = request.POST.get("name")
    color = request.POST.get("color")
    size = request.POST.get("size")
    pattern = request.POST.get("pattern")
    url = request.POST.get("url")
    price = request.POST.get("price") or 0
    special = request.POST.get("special") or 0
    extra = request.POST.get("extra")

    product = Product()
    product.pid = pid
    product.name = name
    product.color = color
    product.size = size
    product.pattern = pattern
    product.url = url
    product.price = price
    product.special = special
    product.extra = extra
    product.save()
    return HttpResponseRedirect("/product/list/")


@login_required()
def product_del(request, id):
    Product.objects.filter(id=id).delete()
    return HttpResponseRedirect("/product/list/")


@login_required()
def product_update(request):
    id = request.POST.get("id")
    pid = request.POST.get("pid")
    name = request.POST.get("name")
    color = request.POST.get("color")
    size = request.POST.get("size")
    pattern = request.POST.get("pattern")
    url = request.POST.get("url")
    price = request.POST.get("price") or 0
    special = request.POST.get("special") or 0
    extra = request.POST.get("extra")

    product = Product.objects.get(id=id)
    product.pid = pid
    product.name = name
    product.color = color
    product.size = size
    product.pattern = pattern
    product.url = url
    product.price = price
    product.special = special
    product.extra = extra
    product.save()
    return HttpResponseRedirect("/product/list/")


# ======== Purchase =====================

@login_required()
def purchase_list(request):
    purchases = Purchase.objects.order_by('-create_time')
    products = Product.objects.order_by('name', 'color', 'size', 'pattern')
    return render_to_response('purchase_list.html', locals())


@login_required()
def purchase_add(request):
    product_id = request.POST.get("product_id")
    quantity = request.POST.get("quantity") or 0
    price = request.POST.get("price")
    comment = request.POST.get("comment")

    product = Product.objects.get(id=product_id)

    if not price:
        quantity = int(quantity)
        price = quantity * product.price

    purchase = Purchase()
    purchase.product = product
    purchase.quantity = quantity
    purchase.price = price
    purchase.comment = comment
    purchase.save()
    return HttpResponseRedirect("/purchase/list/")


@login_required()
def purchase_del(request, id):
    Purchase.objects.filter(id=id).delete()
    return HttpResponseRedirect("/purchase/list/")


@login_required()
def purchase_update(request):
    id = request.POST.get("id")
    product_id = request.POST.get("product_id")
    quantity = request.POST.get("quantity") or 0
    price = request.POST.get("price")
    comment = request.POST.get("comment")

    product = Product.objects.get(id=product_id)

    if not price:
        quantity = int(quantity)
        price = quantity * product.price

    purchase = Purchase.objects.get(id=id)
    purchase.product = product
    purchase.quantity = quantity
    purchase.price = price
    purchase.comment = comment
    purchase.save()
    return HttpResponseRedirect("/purchase/list/")


# ======== Sale =====================

@ip_required
def sale_list(request):
    sales = Sale.objects.order_by('-create_time')
    products = Product.objects.order_by('name', 'color', 'size', 'pattern')
    return render_to_response('sale_list.html', locals())


@ip_required
def sale_add(request):
    product_id = request.POST.get("product_id")
    quantity = request.POST.get("quantity") or 0
    price = request.POST.get("price")
    comment = request.POST.get("comment")

    product = Product.objects.get(id=product_id)

    if not price:
        quantity = int(quantity)
        price = quantity * product.price

    sale = Sale()
    sale.product = product
    sale.quantity = quantity
    sale.price = price
    sale.comment = comment
    sale.save()
    return HttpResponseRedirect("/sale/list/")


@ip_required
def sale_del(request, id):
    Sale.objects.filter(id=id).delete()
    return HttpResponseRedirect("/sale/list/")


@ip_required
def sale_update(request):
    id = request.POST.get("id")
    product_id = request.POST.get("product_id")
    quantity = request.POST.get("quantity") or 0
    price = request.POST.get("price")
    comment = request.POST.get("comment")

    product = Product.objects.get(id=product_id)

    if not price:
        quantity = int(quantity)
        price = quantity * product.price

    sale = Sale.objects.get(id=id)
    sale.product = product
    sale.quantity = quantity
    sale.price = price
    sale.comment = comment
    sale.save()
    return HttpResponseRedirect("/sale/list/")


@ip_required
def quick_input(request):
    if request.method == 'POST':
        client_ip = request.META.get('REMOTE_ADDR', '1.1.1.1')
        data = request.POST.get('data')
        data = data.strip().upper()
        product = Product.objects.filter(extra=data).first()
        if not product:
            return HttpResponse(u'没有对应产品')
        sale = Sale()
        sale.product = product
        sale.quantity = 1
        sale.price = product.current_price

        if product.special > 0:
            sale.comment = u'<span style="color: red">[特价]</span>快速录入(%s)' % client_ip
            sale.is_special = True
            result = u'<span style="color: red">[特价]</span>1份 %s , 录入成功' % product.name
        else:
            sale.comment = u'快速录入(%s)' % client_ip
            sale.is_special = False
            result = u'1份 %s , 录入成功' % product.name

        sale.save()

        return HttpResponse(result)
    return render_to_response('quick_input.html', locals())


@ip_required
def quick_delete(request):
    now = datetime.datetime.now()
    sale = Sale.objects.order_by('-create_time').first()
    if (now - sale.create_time).seconds < 600:
        # 只能删除最近10分钟产生的记录
        sale.delete()
        return HttpResponseRedirect('/quick_input/#username')
    return HttpResponse(u'删除失败,只能删除最近10分钟产生的记录,请联系管理员.<a href="/">返回首页</a>')


def report(request):

    style_blue = xlwt.easyxf('pattern: pattern solid, fore_colour ice_blue;')
    style_orange = xlwt.easyxf('pattern: pattern solid, fore_colour orange;')
    style_red = xlwt.easyxf('pattern: pattern solid, fore_colour red;')

    all_products = Product.objects.order_by('id')

    now = datetime.datetime.now()

    if now.month == 12:
        next_month = 1
    else:
        next_month = now.month + 1

    day_begin = now.replace(hour=0, minute=0, second=0)
    day_end = now.replace(hour=23, minute=59, second=59)
    month_begin = now.replace(day=1, hour=0, minute=0, second=0)
    month_end = now.replace(month=next_month, day=1, hour=0, minute=0, second=0)
    year_begin = now.replace(month=1, day=1, hour=0, minute=0, second=0)
    year_end = now.replace(month=12, day=31, hour=23, minute=59, second=59)

    w = xlwt.Workbook()

    # ----------- day ------------
    sheet_name = u'%d年%d月%d日' % (now.year, now.month, now.day)
    ws = w.add_sheet(sheet_name)

    sales = Sale.objects.filter(create_time__gte=day_begin, create_time__lte=day_end).order_by('create_time')

    time_flag = '%H:%M'

    product_t_price = {}
    product_t_quantity = {}
    special_product_t_price = {}
    special_product_t_quantity = {}
    t_list = []
    product_list = []
    special_product_list = []
    for sale in sales:
        product = sale.product
        t = sale.create_time.strftime(time_flag)
        if t not in t_list:
            t_list.append(t)

        if sale.is_special:
            if product not in special_product_list:
                special_product_list.append(product)
            special_product_t_price[(product.id, t)] = sale.price
            special_product_t_quantity[(product.id, t)] = special_product_t_quantity.get((product.id, t), 0) + int(sale.quantity)
        else:
            if product not in product_list:
                product_list.append(product)
            product_t_price[(product.id, t)] = sale.price
            product_t_quantity[(product.id, t)] = product_t_quantity.get((product.id, t), 0) + int(sale.quantity)

    for product in all_products:
        if product not in product_list + special_product_list:
            product_list.append(product)

    i = 0

    ws.write(i, 1, u'标记')
    ws.write(i, 2, u'品种')
    ws.write(i, 3, u'单价')
    ws.write(i, 4, u'数量')
    ws.write(i, 5, u'小计金额')

    j = 5
    for t in t_list:
        j += 1
        ws.write(i, j, t)

    sum_quantity = 0
    sum_price = 0
    for product in product_list:
        i += 1
        ws.write(i, 1, product.extra)
        ws.write(i, 2, product.name)

        price = product.current_price
        total_quantity = 0
        total_price = 0
        j = 5
        for t in t_list:
            price = product_t_price.get((product.id, t), product.current_price)
            quantity = product_t_quantity.get((product.id, t), 0)
            total_quantity += quantity
            total_price += quantity * price
            j += 1
            if quantity:
                ws.write(i, j, quantity)

        ws.write(i, 3, price)
        ws.write(i, 4, total_quantity)
        ws.write(i, 5, total_price)

        sum_quantity += total_quantity
        sum_price += total_price

    i += 1
    ws.write(i, 3, u'正常总计', style_blue)
    ws.write(i, 4, sum_quantity, style_blue)
    ws.write(i, 5, sum_price, style_blue)

    j = 5
    for t in t_list:
        j += 1
        sub_quantity = 0
        for product in product_list:
            quantity = product_t_quantity.get((product.id, t), 0)
            sub_quantity += quantity
        ws.write(i, j, sub_quantity, style_blue)

    ws.write_merge(1, i-1, 0, 0, u'正常品种')

    # 特价
    i += 1

    ws.write(i, 1, u'标记')
    ws.write(i, 2, u'品种')
    ws.write(i, 3, u'单价')
    ws.write(i, 4, u'数量')
    ws.write(i, 5, u'小计金额')

    j = 5
    for t in t_list:
        j += 1
        ws.write(i, j, t)

    special_start_row = i + 1
    special_sum_quantity = 0
    special_sum_price = 0
    for product in special_product_list:
        i += 1
        ws.write(i, 1, product.extra)
        ws.write(i, 2, product.name)

        price = product.current_price
        total_quantity = 0
        total_price = 0
        j = 5
        for t in t_list:
            price = special_product_t_price.get((product.id, t), product.current_price)
            quantity = special_product_t_quantity.get((product.id, t), 0)
            total_quantity += quantity
            total_price += quantity * price
            j += 1
            if quantity:
                ws.write(i, j, quantity)

        ws.write(i, 3, price)
        ws.write(i, 4, total_quantity)
        ws.write(i, 5, total_price)

        special_sum_quantity += total_quantity
        special_sum_price += total_price

    i += 1
    ws.write(i, 3, u'特价总计', style_orange)
    ws.write(i, 4, special_sum_quantity, style_orange)
    ws.write(i, 5, special_sum_price, style_orange)

    j = 5
    for t in t_list:
        j += 1
        sub_quantity = 0
        for product in special_product_list:
            quantity = special_product_t_quantity.get((product.id, t), 0)
            sub_quantity += quantity
        ws.write(i, j, sub_quantity, style_orange)

    if special_start_row <= i - 1:
        ws.write_merge(special_start_row, i - 1, 0, 0, u'特价品种')

    i += 1
    ws.write(i, 3, u'合计', style_red)
    ws.write(i, 4, sum_quantity + special_sum_quantity, style_red)
    ws.write(i, 5, sum_price + special_sum_price, style_red)

    # ----------- month ------------

    sheet_name = u'%d年%d月' % (now.year, now.month)
    ws = w.add_sheet(sheet_name)

    sales = Sale.objects.filter(create_time__gte=month_begin, create_time__lte=month_end).order_by('create_time')

    time_flag = '%m-%d'

    product_t_price = {}
    product_t_quantity = {}
    special_product_t_price = {}
    special_product_t_quantity = {}
    t_list = []
    product_list = []
    special_product_list = []
    for sale in sales:
        product = sale.product
        t = sale.create_time.strftime(time_flag)
        if t not in t_list:
            t_list.append(t)

        if sale.is_special:
            if product not in special_product_list:
                special_product_list.append(product)
            special_product_t_price[(product.id, t)] = sale.price
            special_product_t_quantity[(product.id, t)] = special_product_t_quantity.get((product.id, t), 0) + int(sale.quantity)
        else:
            if product not in product_list:
                product_list.append(product)
            product_t_price[(product.id, t)] = sale.price
            product_t_quantity[(product.id, t)] = product_t_quantity.get((product.id, t), 0) + int(sale.quantity)

    for product in all_products:
        if product not in product_list + special_product_list:
            product_list.append(product)

    i = 0

    ws.write_merge(i, i + 1, 1, 1, u'标记')
    ws.write_merge(i, i + 1, 2, 2, u'品种')
    ws.write_merge(i, i + 1, 3, 3, u'小计数量')
    ws.write_merge(i, i + 1, 4, 4, u'小计金额')

    j = 4
    for t in t_list:
        j += 1
        ws.write_merge(i, i, j, j + 2, t)
        ws.write(i + 1, j, u'单价')
        ws.write(i + 1, j + 1, u'数量')
        ws.write(i + 1, j + 2, u'金额')
        j += 2
    i += 1

    sum_quantity = 0
    sum_price = 0
    for product in product_list:
        i += 1
        ws.write(i, 1, product.extra)
        ws.write(i, 2, product.name)

        total_quantity = 0
        total_price = 0
        j = 4
        for t in t_list:
            price = product_t_price.get((product.id, t), product.current_price)
            quantity = product_t_quantity.get((product.id, t), 0)
            total_quantity += quantity
            total_price += quantity * price

            j += 1
            ws.write(i, j, price)

            j += 1
            if quantity:
                ws.write(i, j, quantity)

            j += 1
            if quantity:
                ws.write(i, j, quantity * price)

        ws.write(i, 3, total_quantity)
        ws.write(i, 4, total_price)

        sum_quantity += total_quantity
        sum_price += total_price

    i += 1
    ws.write(i, 2, u'正常总计', style_blue)
    ws.write(i, 3, sum_quantity, style_blue)
    ws.write(i, 4, sum_price, style_blue)

    j = 4
    for t in t_list:
        sub_quantity = 0
        sub_price = 0
        for product in product_list:
            price = product_t_price.get((product.id, t), product.current_price)
            quantity = product_t_quantity.get((product.id, t), 0)
            sub_quantity += quantity
            sub_price += quantity * price

        j += 1
        ws.write(i, j, '', style_blue)

        j += 1
        ws.write(i, j, sub_quantity, style_blue)

        j += 1
        ws.write(i, j, sub_price, style_blue)

    ws.write_merge(1, i - 1, 0, 0, u'正常品种')

    # 特价
    i += 1

    ws.write_merge(i, i + 1, 1, 1, u'标记')
    ws.write_merge(i, i + 1, 2, 2, u'品种')
    ws.write_merge(i, i + 1, 3, 3, u'小计数量')
    ws.write_merge(i, i + 1, 4, 4, u'小计金额')

    j = 4
    for t in t_list:
        j += 1
        ws.write_merge(i, i, j, j + 2, t)
        ws.write(i + 1, j, u'单价')
        ws.write(i + 1, j + 1, u'数量')
        ws.write(i + 1, j + 2, u'金额')
        j += 2
    i += 1

    special_start_row = i + 1
    special_sum_quantity = 0
    special_sum_price = 0
    for product in special_product_list:
        i += 1
        ws.write(i, 1, product.extra)
        ws.write(i, 2, product.name)

        total_quantity = 0
        total_price = 0
        j = 4
        for t in t_list:
            price = special_product_t_price.get((product.id, t), product.current_price)
            quantity = special_product_t_quantity.get((product.id, t), 0)
            total_quantity += quantity
            total_price += quantity * price

            j += 1
            ws.write(i, j, price)

            j += 1
            if quantity:
                ws.write(i, j, quantity)

            j += 1
            if quantity:
                ws.write(i, j, quantity * price)

        ws.write(i, 3, total_quantity)
        ws.write(i, 4, total_price)

        special_sum_quantity += total_quantity
        special_sum_price += total_price

    i += 1
    ws.write(i, 2, u'特价总计', style_orange)
    ws.write(i, 3, special_sum_quantity, style_orange)
    ws.write(i, 4, special_sum_price, style_orange)

    j = 4
    for t in t_list:
        sub_quantity = 0
        sub_price = 0
        for product in special_product_list:
            price = special_product_t_price.get((product.id, t), product.current_price)
            quantity = special_product_t_quantity.get((product.id, t), 0)
            sub_quantity += quantity
            sub_price += quantity * price

        j += 1
        ws.write(i, j, '', style_orange)

        j += 1
        ws.write(i, j, sub_quantity, style_orange)

        j += 1
        ws.write(i, j, sub_price, style_orange)

    if special_start_row <= i - 1:
        ws.write_merge(special_start_row, i - 1, 0, 0, u'特价品种')

    i += 1
    ws.write(i, 2, u'合计', style_red)
    ws.write(i, 3, sum_quantity + special_sum_quantity, style_red)
    ws.write(i, 4, sum_price + special_sum_price, style_red)

    # ----------- year ------------

    sheet_name = u'%d年' % now.year
    ws = w.add_sheet(sheet_name)

    sales = Sale.objects.filter(create_time__gte=year_begin, create_time__lte=year_end).order_by('create_time')

    time_flag = '%Y-%m'

    product_t_price = {}
    product_t_quantity = {}
    special_product_t_price = {}
    special_product_t_quantity = {}
    t_list = []
    product_list = []
    special_product_list = []
    for sale in sales:
        product = sale.product
        t = sale.create_time.strftime(time_flag)
        if t not in t_list:
            t_list.append(t)

        if sale.is_special:
            if product not in special_product_list:
                special_product_list.append(product)
            special_product_t_price[(product.id, t)] = special_product_t_price.get((product.id, t), 0) + sale.price
            special_product_t_quantity[(product.id, t)] = special_product_t_quantity.get((product.id, t), 0) + int(sale.quantity)
        else:
            if product not in product_list:
                product_list.append(product)
            product_t_price[(product.id, t)] = product_t_price.get((product.id, t), 0) + sale.price
            product_t_quantity[(product.id, t)] = product_t_quantity.get((product.id, t), 0) + int(sale.quantity)

    for product in all_products:
        if product not in product_list + special_product_list:
            product_list.append(product)

    i = 0

    ws.write_merge(i, i + 1, 1, 1, u'标记')
    ws.write_merge(i, i + 1, 2, 2, u'品种')
    ws.write_merge(i, i + 1, 3, 3, u'小计数量')
    ws.write_merge(i, i + 1, 4, 4, u'小计金额')

    j = 4
    for t in t_list:
        j += 1
        ws.write_merge(i, i, j, j + 1, t)
        ws.write(i + 1, j, u'数量')
        ws.write(i + 1, j + 1, u'金额')
        j += 1
    i += 1

    sum_quantity = 0
    sum_price = 0
    for product in product_list:
        i += 1
        ws.write(i, 1, product.extra)
        ws.write(i, 2, product.name)

        total_quantity = 0
        total_price = 0
        j = 4
        for t in t_list:
            price = product_t_price.get((product.id, t), 0)
            quantity = product_t_quantity.get((product.id, t), 0)
            total_quantity += quantity
            total_price += price

            j += 1
            if quantity:
                ws.write(i, j, quantity)

            j += 1
            if quantity:
                ws.write(i, j, price)

        ws.write(i, 3, total_quantity)
        ws.write(i, 4, total_price)

        sum_quantity += total_quantity
        sum_price += total_price

    i += 1
    ws.write(i, 2, u'正常总计', style_blue)
    ws.write(i, 3, sum_quantity, style_blue)
    ws.write(i, 4, sum_price, style_blue)

    j = 4
    for t in t_list:
        sub_quantity = 0
        sub_price = 0
        for product in product_list:
            price = product_t_price.get((product.id, t), 0)
            quantity = product_t_quantity.get((product.id, t), 0)
            sub_quantity += quantity
            sub_price += price

        j += 1
        ws.write(i, j, sub_quantity, style_blue)

        j += 1
        ws.write(i, j, sub_price, style_blue)

    ws.write_merge(1, i - 1, 0, 0, u'正常品种')

    # 特价
    i += 1

    ws.write_merge(i, i + 1, 1, 1, u'标记')
    ws.write_merge(i, i + 1, 2, 2, u'品种')
    ws.write_merge(i, i + 1, 3, 3, u'小计数量')
    ws.write_merge(i, i + 1, 4, 4, u'小计金额')

    j = 4
    for t in t_list:
        j += 1
        ws.write_merge(i, i, j, j + 1, t)
        ws.write(i + 1, j, u'数量')
        ws.write(i + 1, j + 1, u'金额')
        j += 1
    i += 1

    special_start_row = i + 1
    special_sum_quantity = 0
    special_sum_price = 0
    for product in special_product_list:
        i += 1
        ws.write(i, 1, product.extra)
        ws.write(i, 2, product.name)

        total_quantity = 0
        total_price = 0
        j = 4
        for t in t_list:
            price = special_product_t_price.get((product.id, t), 0)
            quantity = special_product_t_quantity.get((product.id, t), 0)
            total_quantity += quantity
            total_price += price

            j += 1
            if quantity:
                ws.write(i, j, quantity)

            j += 1
            if quantity:
                ws.write(i, j, price)

        ws.write(i, 3, total_quantity)
        ws.write(i, 4, total_price)

        special_sum_quantity += total_quantity
        special_sum_price += total_price

    i += 1
    ws.write(i, 2, u'特价总计', style_orange)
    ws.write(i, 3, special_sum_quantity, style_orange)
    ws.write(i, 4, special_sum_price, style_orange)

    j = 4
    for t in t_list:
        sub_quantity = 0
        sub_price = 0
        for product in special_product_list:
            price = special_product_t_price.get((product.id, t), 0)
            quantity = special_product_t_quantity.get((product.id, t), 0)
            sub_quantity += quantity
            sub_price += price

        j += 1
        ws.write(i, j, sub_quantity, style_orange)

        j += 1
        ws.write(i, j, sub_price, style_orange)

    if special_start_row <= i - 1:
        ws.write_merge(special_start_row, i - 1, 0, 0, u'特价品种')

    i += 1
    ws.write(i, 2, u'合计', style_red)
    ws.write(i, 3, sum_quantity + special_sum_quantity, style_red)
    ws.write(i, 4, sum_price + special_sum_price, style_red)



    # -----------------------------

    # s = StringIO.StringIO()
    # w.save(s)
    #
    # s.seek(0)
    # s = s.read()
    # response = HttpResponse(s, content_type="application/octet-stream")
    # response['Content-Disposition'] = 'attachment; filename=%s.xls' % now.strftime('%Y-%m-%d')
    #
    # return response

    filename = '% s.xls' % now.strftime('%Y-%m-%d')
    w.save('./static/files/%s' % filename)
    return HttpResponseRedirect('/static/files/%s' % filename)


# ======== auth =====================

def loginpage(request):
    return render_to_response('loginpage.html', locals())


def registerpage(request):
    return render_to_response('registerpage.html', locals())


def login(request):
    username = request.REQUEST.get('username', '')
    password = request.REQUEST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
    return HttpResponseRedirect("/")


def logout(request):
    if request.user.is_authenticated():
        auth.logout(request)
    return HttpResponseRedirect("/")


def register(request):
    msg = ""
    username = request.REQUEST.get('username')
    password1 = request.REQUEST.get('password1')
    password2 = request.REQUEST.get('password2')
    if username and password1 and password2:
        if User.objects.filter(username=username):
            msg = "The user name is already registered"
            return render_to_response('registerpage.html', locals())
        if password1 == password2:
            user = User()
            user.username = username
            user.set_password(password1)
            user.save()
            return HttpResponseRedirect("/")
    msg = "You make a mistake, please re-enter"
    return render_to_response('registerpage.html', locals())


@login_required(login_url="/loginpage")
def password(request):
    return render_to_response('password.html', locals())


@login_required(login_url="/loginpage")
def password_reset(request):
    password = request.REQUEST.get('password')
    password1 = request.REQUEST.get('password1')
    password2 = request.REQUEST.get('password2')
    if password and password1 and password2:
        if not request.user.check_password(password):
            msg = "The old password is error!"
            return render_to_response('password.html', locals())
        if password1 == password2:
            request.user.set_password(password1)
            request.user.save()
            return HttpResponseRedirect("/")
    msg = "You make a mistake, please re-enter"
    return render_to_response('password.html', locals())


def write_report(ws, sales, time_flag='%H:%M'):
    product_t_quantity = {}
    product_list = []
    t_list = []
    for sale in sales:
        product = sale.product
        t = sale.create_time.strftime(time_flag)
        if product not in product_list:
            product_list.append(product)
        if t not in t_list:
            t_list.append(t)
        product_t_quantity[(product.id, t)] = product_t_quantity.get((product.id, t), 0) + int(sale.quantity)

    j = 5
    for t in t_list:
        j += 1
        ws.write(0, j, t)

    sum_quantity = 0
    sum_price = 0
    i = 0
    for product in product_list:
        i += 1
        ws.write(i, 0, i)
        ws.write(i, 1, product.extra)
        ws.write(i, 2, product.name)

        price = product.price
        total_quantity = 0
        total_price = 0
        j = 5
        for t in t_list:
            quantity = product_t_quantity.get((product.id, t), 0)
            total_quantity += quantity
            total_price += quantity * price
            j += 1
            if quantity:
                ws.write(i, j, quantity)

        ws.write(i, 3, total_quantity)
        ws.write(i, 4, price)
        ws.write(i, 5, total_price)

        sum_quantity += total_quantity
        sum_price += total_price

    i += 1
    ws.write(i, 3, sum_quantity)
    ws.write(i, 5, sum_price)

    j = 5
    for t in t_list:
        j += 1
        sub_quantity = 0
        for product in product_list:
            quantity = product_t_quantity.get((product.id, t), 0)
            sub_quantity += quantity
        ws.write(i, j, sub_quantity)

