
from django.conf.urls import patterns, include, url
from views import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns(
    '',
    ('^$', index),
    ('^index/$', index),

    ('^admin/', include(admin.site.urls)),

    ('^product/list/$', product_list),
    ('^product/add/$', product_add),
    ('^product/del/(\w+)/$', product_del),
    ('^product/update/$', product_update),

    ('^purchase/list/$', purchase_list),
    ('^purchase/add/$', purchase_add),
    ('^purchase/del/(\w+)/$', purchase_del),
    ('^purchase/update/$', purchase_update),

    ('^sale/list/$', sale_list),
    ('^sale/add/$', sale_add),
    ('^sale/del/(\w+)/$', sale_del),
    ('^sale/update/$', sale_update),

    ('^quick_input/$', quick_input),
    ('^quick_delete/$', quick_delete),
    ('^report/$', report),

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
