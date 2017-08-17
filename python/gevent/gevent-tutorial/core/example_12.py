import socket
print socket.socket

print "After monkey patch"
from gevent import monkey
monkey.patch_socket()
print socket.socket

import select
print select.select
print "After monkey patch"
monkey.patch_select()
print select.select
