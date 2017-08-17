#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from datetime import datetime, timedelta

from django.http import HttpResponse
from django.shortcuts import render, render_to_response, redirect
from django.views.decorators.cache import never_cache

from constance import config

# Create your views here.

@never_cache
def index(request):
    # django-constance
    print 'THE_ANSWER =', config.THE_ANSWER
    return render_to_response('index.html', {'config': config})

@never_cache
def time(request):
    date_time = datetime.now()
    data = dict(datetime = str(date_time))
    return HttpResponse(json.dumps(data))
