#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('polls',
    url(r'^$', 'views.index'),
    url(r'^choice$', 'views.choice'),
)
