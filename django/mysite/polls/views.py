#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.views.decorators.cache import never_cache

from polls.models import Poll, Choice

# Create your views here.

@never_cache
def index(request):
    polls = Poll.objects.all()
    return render_to_response('polls/index.html', {'polls': polls})

@never_cache
def choice(request):
    poll_id = int(request.REQUEST.get('poll_id', 0))
    choices = Choice.objects.filter(poll=poll_id)
    return render_to_response('polls/choice.html', {'choices': choices})
