#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from utils.core.db_manager import SplitTableManager

# Create your models here.

class Other(models.Model):
    title = models.CharField(max_length=200)
    content = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    # objects = SplitTableManager(using='db_other')
    # def save(self):
    #     self._meta.db_name = Other.objects.gen_split_table_name()
    #     super(Other, self).save()

    def __unicode__(self):
        return self.title

    class Meta:
        db_table = 'other'
