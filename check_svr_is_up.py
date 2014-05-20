'''
Script to notify admin that server is down
'''

import urllib2
import json
from datetime import datetime

import smtplib
from email.mime.text import MIMEText
import string

import settings

# If everything is going well, then nothing happens.

try:
  f = urllib2.urlopen('http://localhost/is_alive/')
  status = json.loads(f.read())
except urllib2.URLError:
  status = False

if status is not True:
  error_msg = "[ %s ] ERROR Server Down" % datetime.now()
  f = open("logs/svr.log", "a")
  f.write(error_msg)

  # Open a plain text file for reading.  For this example, assume that
  # the text file contains only ASCII characters.
  msg = MIMEText(error_msg)
  
  # me == the sender's email address
  # you == the recipient's email address
  sender = "svr@%s" % settings.DOMAIN
  recipients = settings.ADMIN_EMAILS
  
  msg['Subject'] = error_msg
  msg['From'] = sender
  msg['To'] = string.join(recipients, ", ")

  # Send the message via our own SMTP server, but don't include the
  # envelope header.
  s = smtplib.SMTP('localhost')
  s.sendmail(sender, recipients, msg.as_string())
  s.quit()
