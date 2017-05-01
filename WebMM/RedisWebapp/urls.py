from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$',login),
    url(r'^regist/$',regist),
    url(r'^index/$',index),
    url(r'^inset/$',inset),
]
