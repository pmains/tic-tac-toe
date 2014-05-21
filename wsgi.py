'''
Render pages to be served by WSGI-compatible server
'''

import os, sys
sys.path.append(os.path.dirname(__file__))
import settings

from urls import urls
import re
import handle_static
from settings import STATIC_FOLDER

def application(environ, start_response):  
  '''Returns rendered pages and files to be served'''

  # Find the path to be served and by which HTTP method
  path = environ['PATH_INFO']
  method = environ['REQUEST_METHOD']

  # If data sent with request, read data in order to pass to request handler
  data = None
  try:
    content_length = int(environ.get('CONTENT_LENGTH', 0))
  except ValueError:
    content_length = 0
  if content_length > 0:
    data = environ['wsgi.input'].read(content_length)

  # Get HTTP response from the appropriate request handler
  response = None
  if re.search("^/%s" % STATIC_FOLDER, path) is not None:
    response = handle_static.do_GET(path)
  else:
    response = handle(path, method, data)

  # For discussion of start_response, see http://stackoverflow.com/questions/16774952/wsgi-whats-the-purpose-of-start-response-function
  start_response(response['status'], response['response_headers'])
  return [response['response_body']]

def handle(path, method, data=None):
  '''Handle non-static content'''
  # Find url from urls.py
  for url in urls:
    # HTTP method must match that specified by urls entry
    if method.upper() != url['method']:
      continue

    # Determine if path matches that specified by urls entry
    m = re.match(url['path'], path)
    if m:
      controller = url['controller']
      # Pass data argument to request controller 
      if data is None:
        return controller(m)
      else:
        return controller(m, data)

  # If matching urls entry not found, return 404 
  return handle_static.not_found_404()
