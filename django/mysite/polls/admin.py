#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin

from polls.models import Poll, Choice

admin.site.register(Poll)
admin.site.register(Choice)
