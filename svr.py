'''
Use Python's WSGI Reference implementation to run
'''

from wsgiref.simple_server import make_server
from wsgi import application

httpd = make_server('localhost', 85, application)
httpd.serve_forever()
