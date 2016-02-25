# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from models import *
import os
import uuid


def index(request):
    return render_to_response('index.html', locals())


# ======== Product =====================

@login_required()
def product_list(request):
    products = Product.objects.all()
    return render_to_response('product_list.html', locals())


@login_required()
def product_add(request):
    pid = request.POST.get("pid")
    name = request.POST.get("name")
    color = request.POST.get("color")
    size = request.POST.get("size")
    pattern = request.POST.get("pattern")
    url = request.POST.get("url")
    price = request.POST.get("price")
    product = Product()
    product.pid = pid
    product.name = name
    product.color = color
    product.size = size
    product.pattern = pattern
    product.url = url
    product.price = price
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
    price = request.POST.get("price")
    product = Product.objects.get(id=id)
    product.pid = pid
    product.name = name
    product.color = color
    product.size = size
    product.pattern = pattern
    product.url = url
    product.price = price
    product.save()
    return HttpResponseRedirect("/product/list/")


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

