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

class MainHandler(webapp2.RequestHandler):
    def get(self):

        #setup check
        try:
            bucket_name = grand.config['www_bucket']
        except KeyError:
            return self.redirect('/grand/setup')


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
            self.response.headers['Cache-Control'] = 'no-cache'
            self.response.headers['Access-Control-Allow-Origin'] = '*'
            self.response.headers['Vary'] = 'Origin'
            self.response.headers['Content-Type'] =  stat.content_type 
            self.response.headers['Content-Length'] =  str(stat.st_size)
            
            if( stat.content_type.startswith('image') and grand.config['thumbnail_enabled'] == 'True' ):
                
                #use image api instead of serving like text
                filename = '/gs'+filename
                #img = images.Image(filename=filename)
                blob_key = blobstore.create_gs_key(filename)

                #self.response.headers['Content-Type'] =  'text/plain'
                #self.response.write(blob_key)
                #return
                
                resizeCommand = path[1]
                if(resizeCommand==None):
                    resizeCommand = ''
                
                # TODO: server proxy cached data from this url rather than redirecting.    
 
                # this might actually be sufficient since it's doing exactly what it's supposed to.
                return self.redirect( images.get_serving_url(blob_key) + resizeCommand, self.response) 
            
            
                #result = urlfetch.fetch(
                #    url= images.get_serving_url(blob_key) + resizeCommand ,
                #    deadline=60*10, #seconds
                #    follow_redirects=True,
                #)
                
                #todo: store result.content into datastore Thumbnail object.
                #result.content
                #todo: serve that file


            else:
                self.response.write(gcs_file.read())
                return self.response
            
            gcs_file.close()


        except gcs.NotFoundError:
            return webapp2.abort(404)

class HomeHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write("""<!DOCTYPE html>
    <html>
	<head>
	    <title>cdn home page</title>
	    <meta name="google-site-verification" content="_aT7zb6Uiuu9lrN4Fii93fK4w4OLUj8EgCOOetH6ig4" />
	</head>
	<body>
            hi there, this is a CDN server. This page is a placeholder to host google property owndership metadata.
            
	</body>
    </html>
    
""")

app = webapp2.WSGIApplication([
    ('/' , HomeHandler),
    ('/grand/test' , test.MainHandler),
    ('/.+', MainHandler),

], debug=True)

