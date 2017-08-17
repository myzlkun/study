#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import gevent
from gevent import monkey

monkey.patch_all()

import sys

# urls = ['http://www.google.com', 'http://www.yandex.ru', 'http://www.python.org']
urls = ['http://www.baidu.com', 'http://www.yandex.ru', 'http://www.python.org']


if sys.version_info[0] == 3:
    from urllib.request import urlopen
else:
    from urllib2 import urlopen


def print_head(url):
    print('Starting %s' % url)
    data = urlopen(url).read()
    print('%s: %s bytes: %r' % (url, len(data), data[:50]))

jobs = [gevent.spawn(print_head, url) for url in urls]

gevent.wait(jobs)
