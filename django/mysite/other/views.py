#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.views.decorators.cache import never_cache

from other.models import Other

# Create your views here.

@never_cache
def index(request):
    others = Other.objects.all()
    return render_to_response('other/index.html', {'others': others})
