#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

def serve_page(env, start_response):
    paragraph = '''
        Lorem ipsum dolor sit amet,
        consectetur adipisicing elit,
        sed do eiusmod tempor incididunt ut labore et
        dolore magna aliqua. Ut enim adminim veniam,
        quis nostrud exercitation ullamco laboris nisi ut aliquip
        ex ea commodo consequat.
        Duis aute irure dolor in reprehenderit in
        voluptate velit esse cillum dolore eu fugiat nulla pariatur.
        Excepteur sint occaecat cupidatat non proident,
        sunt in culpa qui officia deserunt mollit anim id est laborum.
    '''
    page = '''
        <html>
            <head>
                <title>Static Page</title>
            </head>
            <body>
                <h1>Static Content</h1>
                <p>%s</p>
            </body>
        </html>
    ''' % (paragraph * 10)

    start_response('200 OK', [('Content-Type', 'text/html')])
    return [page]

if __name__ == '__main__':
    def usage():
        print 'usage:', sys.argv[0], 'gevent|threaded CONCURRENCY'
        sys.exit(1)

    if len(sys.argv) != 3 or sys.argv[1] not in ['gevent', 'threaded']:
        usage()

    try:
        concurrency = int(sys.argv[2])
    except ValueError:
        usage()

    if sys.argv[1] == 'gevent':
        from gevent.wsgi import WSGIServer
        WSGIServer(['127.0.0.1', 8000], serve_page, log=None, spawn=concurrency).serve_forever()
    else:
        from paste import httpserver
        httpserver.serve(serve_page, host='127.0.0.1', port=8000, use_threadpool=True, threadpool_workers=concurrency)
