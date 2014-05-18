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

import webapp2
import os
import cloudstorage as gcs
import grand
import unittest
from google.appengine.api import app_identity
from google.appengine.api import urlfetch 
import re
import json
import urllib2
    
class MainHandler(webapp2.RequestHandler , unittest.TestCase):

    def p(self,s):
        self.response.write(s+'\n')
        
    def testFiles(self):
            self.p('\nTrying to open cloud storage file data/a.jpg')
            gsc_file = gcs.open( '/%s/%s' % ( grand.config['www_bucket'] , 'data/a.jpg'  ) , 'r')
            self.p('\tFile opened for reading.')
            gsc_file.close()

            
    def get(self):

        self.response.headers['Content-Type'] =  'text/plain'

        # config template
        #self.p('\nCreating config in datastore.')
        
        self.p('\nTesting config system.')
        self.p( '\t.thumbnail_bucket exists: ' + str( grand.config.has_key('non_existent_key') ) )
        self.p( "\t.thumbnail_bucket: " + grand.config['thumbnail_bucket'] )
        self.p( "\t.thumbnail_enabled: " + grand.config['thumbnail_enabled'] )

        self.assertFalse( grand.config.has_key('non_existent_key') )
        try:
            self.p( '\t.non_existent_key: ' + grand.config['non_existent_key'] )
            self.p('\tKeyError not raised.')
        except KeyError:
            self.p('\tKeyError rightfully raised.')
        finally:
            self.p('\tSuccess.')

        self.testFiles()

        self.p('\nattempting to download image')


        result = urlfetch.fetch(
            url='http://cdn.jtn.im/000017.jpg=s8',
            deadline=120,
            follow_redirects=True,
        )
        
        self.response.write(result.status_code)
        self.response.write('\n\n')
        self.response.write(result.headers)
        self.response.write('\n\n')
        self.response.write( len(result.content) )
        self.response.write('\n\n')
        

        #result = urlfetch.fetch('http://%s:%s/000017.jpg' % (os.environ["SERVER_NAME"],os.environ["SERVER_PORT"]))

        #self.assertEqual(result.status_code , 200)
        #self.assertTrue( 0 < len(result.content) )
        
        #self.p('\nattempting to download image with resizing argument')
        #result = urlfetch.fetch('http://%s:%s/data/a.jpg=s32' % (os.environ["SERVER_NAME"],os.environ["SERVER_PORT"]))
        #self.assertEqual(result.status_code , 200)
        #self.assertTrue( 0 < len(result.content) )
        
        #self.p('\nattempting to download image with invalid resizing argument')
        #response = urlfetch.fetch('http://%s:%s/data/a.jpg=s32' % (os.environ["SERVER_NAME"],os.environ["SERVER_PORT"]))
        #self.assertEqual(response.status_code , 200)
        #self.assertTrue( 0 < len(result.content) )
        #self.p( json.dumps(dir(result)) )
        #self.response.write(response )
        # WHERE IS THE REDIRECT HEADER?
        
        
