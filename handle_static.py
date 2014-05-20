'''
Serves static files for hypnos test server
This should not be used in production
'''
from settings import HOME_DIR, STATIC_DIR

import codecs
import re
import mimetypes
from handle import response, not_found_404, OK
from os import curdir, sep

# mimetypes to be read as binary files
binary_mimetypes = [
  "application/zip",
  "image/gif",
  "image/png",
  "image/x-png",
  "image/jpeg",
  "image/pjpeg",
  "application/x-font-woff",
  "application/x-font-ttf",
  "application/vnd.ms-fontobject",
  "image/svg+xml"
]

# extensions of mimetypes which cannot be guessed by Python
mimetypes_by_ext = {
  "woff": "application/x-font-woff",
  "tff":  "application/x-font-ttf",
  "eot":  "application/vnd.ms-fontobject",
  "svg":  "image/svg+xml"
}
  
def do_GET(path):
  '''Returns response to GET requests'''
  status = OK
  mode = "r"

  # find location of the file to be served
  m = re.match(r'/www/(?P<location>.*)$', path)
  location = STATIC_DIR + m.group('location')
  content_type = mimetypes.guess_type(location)[0]

  # if Python cannot guess the mimetype
  if content_type is None:
    # extract the file extension
    m = re.match(r'.*\.(?P<ext>\w+)$', location)
    if m is not None:
      # look to see if extension is known
      ext = m.group("ext")
      if ext in mimetypes_by_ext:
        content_type = mimetypes_by_ext[ext]

  # render x-png files as png
  if content_type == "image/x-png":
    content_type = "image/png"
  # read binary files are binary files
  if content_type in binary_mimetypes:
    mode = "rb"

  # by default, response body is empty
  response_body = ""
  try:
    # HTML pages escape non-ascii characters
    if content_type == "text/html":
      f = codecs.open(location, encoding="utf-8")
      response_body = f.read().encode("ascii", "xmlcharrefreplace")
      f.close()
    # otherwise, serve files as-is
    else:
      f = open(location, mode)
      response_body = f.read()
      f.close()
  # if file cannot be served, return 404 error
  except IOError:
    return not_found_404(path)
  
  return response(status, content_type, response_body)
