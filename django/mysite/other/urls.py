#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('other',
    url(r'^$', 'views.index'),
)
