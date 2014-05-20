'''
Includes common functions and variables needed for rendering HTTP responses
'''

import pystache
import codecs
from os import curdir, sep
from settings import HOME_DIR, TEMPLATE_DIR, FILE_EXTENSION, STATIC_DIR

# Response mimetypes
HTML = 'text/html'
TEXT = 'text/plain'
JSON = 'application/json'

# HTTP standard response codes
OK = '200 OK'
FOUND = '302 Found' # Used for redirects
NOT_FOUND = '404 Not Found'
CONFLICT  = '409 Conflict'
ERROR = '500 Internal Server Error'

def response(status, content_type, response_body):
  '''Return HTTP response, including response code (status), headers and body'''
  # Set response headers
  response_headers = [
    ('Content-Type', content_type),
    ('Content-Length', str(len(response_body)))
  ]

  # Return HTTP response
  return { 'status': status, 'response_headers': response_headers, 'response_body': response_body }

def redirect(location):
  '''Returns response that redirects to a different URL'''
  # Set response headers
  response_headers = [
    ('Location', location),
    ('Content-Type', TEXT)
  ]
  # Return HTTP redirect response
  return { 'status': FOUND, 'response_headers': response_headers, 'response_body': '' }

def not_found_404(location=None):
  '''Returns 404 Response'''
  if location is not None:
    print "Could not find %s" % location

  # Read and render 404 response template
  f = open(STATIC_DIR + '404.html')
  response_body = f.read()
  f.close()
  
  return response(NOT_FOUND, HTML, response_body)

def render_template_response(context, template):
  '''
  Renders template and returns HTTP response.
  Takes data to be used by template (context) and template name (template) as arguments.
  '''
  content_type = HTML
  location = TEMPLATE_DIR + template
  
  try:
    f = codecs.open(location, encoding="utf-8")
    template_content = f.read()
    f.close()
  except IOError:
    # If template cannot be read, return 404 error
    return not_found_404(location)

  # Render template
  renderer = pystache.Renderer(search_dirs=TEMPLATE_DIR, file_extension=FILE_EXTENSION)
  rendered_template = renderer.render(template_content, context, string_encoding="utf-8")
  response_body = rendered_template.encode('ascii', 'xmlcharrefreplace')

  # Return response with rendered template as the reponse_body
  return response(OK, content_type, response_body)
