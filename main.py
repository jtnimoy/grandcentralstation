#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
# Copyright 2014 Joshua T. Nimoy
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import sys
sys.path.insert(0,'lib')

import logging
import cloudstorage as gcs
import webapp2
import re
from google.appengine.api import urlfetch
from google.appengine.api import app_identity
from google.appengine.api import images
from google.appengine.ext import blobstore
import mimetypes
import urllib
import json
import os

import grand
import test

# Retry can help overcome transient urlfetch or GCS issues, such as timeouts.
my_default_retry_params = gcs.RetryParams(initial_delay=0.2,
                                          max_delay=5.0,
                                          backoff_factor=2,
                                          max_retry_period=15)
gcs.set_default_retry_params(my_default_retry_params)



    
class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write("hi there")
        
        
app = webapp2.WSGIApplication([
    ('/grand/test' , test.MainHandler),
    ('/.+', MainHandler),

], debug=True)

