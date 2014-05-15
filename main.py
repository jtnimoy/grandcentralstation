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

    def serveProxyCached(self , url):
        #does the url not exist in the bucket?
        try:
            gcs.stat(url)
        except NotFoundError:
            #download the data and store it into the bucket.
            result = urlfetch.fetch(url)
            if result.status_code == 200:
                #todo: store it
                pass
            else:
                return webapp2.abort(510)
            
        #todo: serve that file.
    
    def get(self):
        bucket_name = os.environ.get('BUCKET_NAME' , app_identity.get_default_gcs_bucket_name() )
        decodedPath = urllib.unquote(self.request.path)

        # split out the image thumbnail command
        matches = re.match( '^(?P<part1>.*?)(?P<part2>=.*?)?$' , decodedPath )
        path = [
            matches.group('part1'), #classic url
            matches.group('part2')  #image resize command, like s=256-c
        ]
        
        filename = '/' + bucket_name + path[0]

        # fix for indices.
        if path[0][-1] == '/':
            filename += 'index.html'
        
        #read file
        try:
            
            #first error might be directory, so provide a second try
            try:
                gcs_file = gcs.open(filename)
            except gcs.NotFoundError:
                filename += '/index.html'
                gcs.stat(filename)
                # trailing slash redirect happens if stat is success
                return self.redirect(urllib.quote( path[0] + '/'), code=301)
                
            stat = gcs.stat(filename)

            # TODO: saw an html file served as plain. perhaps google's mime interp is unconventional
            self.response.headers['Content-Type'] =  stat.content_type 
            self.response.headers['Content-Length'] =  str(stat.st_size)
            self.response.headers['Cache-Control'] = 'public, max-age=31536000'
            
            if( stat.content_type.startswith('image')):
                
                #use image api instead of serving like text
                filename = '/gs'+filename
                img = images.Image(filename=filename)
                blob_key = blobstore.create_gs_key(filename)

                #self.response.headers['Content-Type'] =  'text/plain'
                #self.response.write(blob_key)
                #return
                
                resizeCommand = path[1]
                if(resizeCommand==None):
                    resizeCommand = ''
                
                # TODO: server proxy cached data from this url rather than redirecting.    
                return self.redirect( images.get_serving_url(blob_key) + resizeCommand )
                
            else:
                self.response.write(gcs_file.read())
            gcs_file.close()

        except gcs.NotFoundError:
            return webapp2.abort(404)
            

class RootHandler(webapp2.RequestHandler):
    def get(self):
        if os.environ.get('SERVER_SOFTWARE').startswith('Development'):
            self.response.write('''<h1>It works!</h1>
<div><a href="http://github.com/jtnimoy/grandcentralstation">GrandCentralStation</a>,
a static  media server for GoogleCloudStorage.</div>
<a href="grand/test">Unit test me.</a>
            ''')
            
            



app = webapp2.WSGIApplication([
    ('/grand/test' , test.MainHandler),
    ('/.+', MainHandler),
    ('/', RootHandler),

], debug=True)

