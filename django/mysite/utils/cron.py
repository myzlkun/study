#!/usr/bin/env python
from datetime import datetime

def my_scheduled_job():
    now = datetime.now()
    print 'my test job: %s' % now.strftime('%Y-%m-%d %H:%M:%s')
