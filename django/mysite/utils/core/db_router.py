#!/usr/bin/env python
# -*- coding: utf-8 -*-

class MasterSlaveRouter(object):
    def db_for_read(self, model, **hints):
        return self.__app_router(model)

    def db_for_write(self, model, **hints):
        return self.__app_router(model)

    def allow_relation(self, obj1, obj2, **hints):
        # if obj1._meta.app_label == obj2._meta.app_label:
        if self.__app_router(obj1) == self.__app_router(obj2):
            return True
        return None

    def allow_syncdb(self, db, model):
        return self.__app_router(model) == db

    def __app_router(self, model):
        if model._meta.app_label == 'polls':
            return 'db_main'
        elif model._meta.app_label == 'other':
            return 'db_other'
        else:
            return 'default'
