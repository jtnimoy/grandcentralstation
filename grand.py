#!/usr/bin/env python
#
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

from google.appengine.api import app_identity
from google.appengine.api import namespace_manager
from google.appengine.ext import db
import os
import webapp2
import cloudstorage as gcs


class ns:
    '''manage namespace'''
    namespaceStack = []
    @staticmethod
    def push():
        ns.namespaceStack.append(namespace_manager.get_namespace() )

    @staticmethod
    def pop():
        namespace_manager.set_namespace( ns.namespaceStack.pop() )

    @staticmethod
    def begin():
        ns.push()
        namespace_manager.set_namespace('grandcentralstation')
        
    @staticmethod
    def end():
        ns.pop()


        
class Setting(db.Model):
    value = db.StringProperty()


class Thumbnail(db.Model):
    content = db.StringProperty()
    mime = db.StringProperty()


class ConfigurationSimplifier:
    def has_key(self,key):
        try:
            v = self[key]
            return True
        
        except:
            return False
    
    def __getitem__(self,key):
        ns.begin()
        try:
            q = Setting.get_by_key_name(key)
            ns.end()
            return (q.value)
        except AttributeError:
            raise KeyError("grand.config key not found: '%s'" % key)

    def __setitem__(self, key,val):
        ns.begin()
        s = Setting( key_name=key )
        s.value = val
        s.put()
        ns.end()



config = ConfigurationSimplifier()

class SetupHandler(webapp2.RequestHandler):
    def get(self):

        self.response.write('<h1>grandcentralstation</h1>')

        config['www_bucket'] = os.environ.get('BUCKET_NAME' , app_identity.get_default_gcs_bucket_name() )
        config['thumbnail_enabled'] = 'True'

        filenames = [
            {'name':'data/a.jpg','mime':'image/jpeg'},
            {'name':'data/index.html','mime':'text/html'},
            {'name':'data/a b/index.html','mime':'text/html'},
        ]

        if os.environ.get('SERVER_SOFTWARE').startswith('Development'):
            self.response.write('\nDev~ detected. Adding dummy files.\n')
            #set up test bucket data    
            for file in filenames:
                data = open(file['name'],'r')
                gcs_file = gcs.open( '/%s/%s' % ( config['www_bucket'] ,file['name']) ,'w',content_type=file['mime'])
                gcs_file.write(data.read())
                data.close()
                gcs_file.close()
                self.response.write('\tAdded file \'%s\'.\n' % data.name)


        self.response.write('<p>I detected a fresh deploy so I populated the datastore with a default configuration.</p>')

