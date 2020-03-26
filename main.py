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
# limitations ODunder the License.
#

import sys
sys.path.insert(0,'lib')

import flask
import os
import urllib
import re

from google.cloud import storage
from google.cloud.storage import Blob


app = flask.Flask(__name__)

    
@app.route('/')
def root():
    config = {}
    
    config['www_bucket'] = os.environ.get('BUCKET_NAME' , '' )
    config['thumbnail_enabled'] = 'True'


    #setup check
    try:
        bucket_name = config['www_bucket']
    except KeyError:
        return "no bucket found"

        
    decodedPath = urllib.parse.unquote(flask.request.path)

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

    storage_client = storage.Client()
        
    #read file
    try:
            
        #first error might be directory, so provide a second try
        try:
            blob_file = Blob(filename)
        except:
            filename += '/index.html'
            Blob(filename)
            # trailing slash redirect happens if stat is success
            return redirect(urllib.parse.quote( path[0] + '/'), code=301)
                
        stat = Blob(filename)


        # TODO: saw an html file served as plain. perhaps google's mime interp is unconventional
        resp = flask.Response()
        
        resp.headers['Content-Type'] =  stat.content_type 
        resp.headers['Content-Length'] =  str(stat.st_size)
        resp.headers['Cache-Control'] = 'no-cache'
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Vary'] = 'Origin'

        return resp

        """
        if( stat.content_type.startswith('image') and config['thumbnail_enabled'] == 'True' ):
                
            #use image api instead of serving like text
            filename = '/gs'+filename
            img = images.Image(filename=filename)
            blob_key = blobstore.create_gs_key(filename)

                
            resizeCommand = path[1]
            if(resizeCommand==None):
                resizeCommand = ''
                
            # TODO: server proxy cached data from this url rather than redirecting.    
 
            # this might actually be sufficient since it's doing exactly what it's supposed to.
            return redirect( images.get_serving_url(blob_key) + resizeCommand, resp ) 
            
            
        else:
            resp.headers['body'] = blob_file.read()
            blob_file.close()

        
        return resp
"""

    except:
        return '',404
            


def MainHandler_get():
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
            return redirect(urllib.parse.quote( path[0] + '/'), code=301)
                
        stat = gcs.stat(filename)

        # TODO: saw an html file served as plain. perhaps google's mime interp is unconventional
        resp = flask.Response()
        
        resp.headers['Content-Type'] =  stat.content_type 
        resp.headers['Content-Length'] =  str(stat.st_size)
        resp.headers['Cache-Control'] = 'no-cache'
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Vary'] = 'Origin'
            
        #if( stat.content_type.startswith('image') and config['thumbnail_enabled'] == 'True' ):
        #        
        #    #use image api instead of serving like text
        #    filename = '/gs'+filename
        #    img = images.Image(filename=filename)
        #    blob_key = blobstore.create_gs_key(filename)

                
        #    resizeCommand = path[1]
        #    if(resizeCommand==None):
        #        resizeCommand = ''
                
            # TODO: server proxy cached data from this url rather than redirecting.    
 
            # this might actually be sufficient since it's doing exactly what it's supposed to.
        #    return redirect( images.get_serving_url(blob_key) + resizeCommand, self.response ) 
            
            
        #else:
        #    self.response.write(gcs_file.read())
        #    gcs_file.close()

    except gcs.NotFoundError:
        return webapp2.abort(404)
            

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
    
