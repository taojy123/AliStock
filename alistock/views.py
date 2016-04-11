# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from models import *
import xlwt
import os
import uuid


def index(request):
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
    extra = request.POST.get("extra")

    product = Product()
    product.pid = pid
    product.name = name
    product.color = color
    product.size = size
    product.pattern = pattern
    product.url = url
    product.price = price
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
    extra = request.POST.get("extra")

    product = Product.objects.get(id=id)
    product.pid = pid
    product.name = name
    product.color = color
    product.size = size
    product.pattern = pattern
    product.url = url
    product.price = price
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

@login_required()
def sale_list(request):
    sales = Sale.objects.order_by('-create_time')
    products = Product.objects.order_by('name', 'color', 'size', 'pattern')
    return render_to_response('sale_list.html', locals())


@login_required()
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


@login_required()
def sale_del(request, id):
    Sale.objects.filter(id=id).delete()
    return HttpResponseRedirect("/sale/list/")


@login_required()
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


@login_required()
def quick_input(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        data = data.strip().upper()
        product = Product.objects.filter(extra=data).first()
        if not product:
            return HttpResponse(u'没有对应产品')
        sale = Sale()
        sale.product = product
        sale.quantity = 1
        sale.price = product.price
        sale.comment = u'%s 快速录入' % request.user.username
        sale.save()
        result = u'1份 %s , 录入成功' % product.name
        return HttpResponse(result)
    return render_to_response('quick_input.html', locals())


@login_required()
def report(request):

    w = xlwt.Workbook()
    ws = w.add_sheet('day')

    ws.write(1, 1, u'序号')
    ws.write(1, 2, u'标记')
    ws.write(1, 3, u'品种')
    ws.write(1, 4, u'出货量')
    ws.write(1, 5, u'时间明细')

    # w.save('mini.xls')

    return render_to_response('quick_input.html', locals())


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

