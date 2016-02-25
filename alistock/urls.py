
from django.conf.urls import patterns, include, url
from views import *
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
urlpatterns = patterns('',
    ('^$', index),
    ('^index/$', index),

    ('^product/list/$', product_list),
    ('^product/add/$', product_add),
    ('^product/del/(\w+)/$', product_del),
    ('^product/update/$', product_update),

    ('^loginpage/$', loginpage),
    ('^login/$', login),
    ('^logout/$', logout),
    ('^register/$', register),
    ('^password/$', password),
    ('^password/reset/$', password_reset),

)
# This will work if DEBUG is True
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
