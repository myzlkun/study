#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime

class SplitTableManager(models.Manager):
    db_table_name_original = None
    db_table_name_split = None

    def __init__(self, using=None):
        self.using = using
        super(SplitTableManager, self).__init__()

    def gen_split_table_name(self):
        if not self.db_table_name_original:
            self.db_table_name_original = self.model._meta.db_table
        self.db_table_name_split = self.db_table_name_original + datetime.now().strftime('_%Y%m%d')
        if self.model._meta.db_table != self.db_table_name_split:
            self.model._meta.db_table = self.db_table_name_split
            from django.db import connections
            using = self.using or 'default'
            conn = connections[using]
            cursor = conn.cursor()
            cursor.execute('SHOW TABLES LIKE %s', [self.db_table_name_split])
            if not cursor.fetchone():
                from django.db import transaction
                from django.core.management.color import no_style
                sql, references = connections[using].creation.sql_create_model(self.model, no_style())
                for statement in sql:
                    connections[using].cursor().execute(statement)
                transaction.commit_unless_managed()
        return self.db_table_name_split

    def get_query_set(self):
        self.gen_split_table_name()
        return super(SplitTableManager, self).get_query_set()
