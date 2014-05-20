'''
Include application-specific settings
'''

from os import curdir, sep

DOMAIN = "localhost"
ADMIN_EMAILS = [ "peter.mains@gmail.com" ]

HOME_DIR = curdir + sep
TEMPLATE_DIR = HOME_DIR + "templates" + sep
STATIC_FOLDER = "www"
STATIC_DIR = HOME_DIR + STATIC_FOLDER + sep

FILE_EXTENSION = "mst"
