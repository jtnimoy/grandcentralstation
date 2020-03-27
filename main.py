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

    
@app.route('/<b>')
def root(b):
    textout = ''
    thumbnail_enabled = os.environ.get('THUMBNAIL_ENABLED' )
    storage_client = storage.Client()


    #setup check
    bucket_name = os.environ.get('BUCKET_NAME' )
    if bucket_name == '':    
        return "no bucket name in $BUCKET_NAME",200
    
    bucket = storage_client.bucket(bucket_name,os.environ.get('PROJECT_NAME'))
    if not bucket.exists():
        return "bucket doesn't exist", 200

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

    if True:
        #first error might be directory, so provide a second try
        
        blob = bucket.get_blob(path[0])
        if blob == None:
            # trailing slash redirect happens if blob is success
            return redirect(urllib.parse.quote( path[0] + '/index.html'), code=301)
            
        # TODO: saw an html file served as plain. perhaps google's mime interp is unconventional
        resp = flask.Response()

        resp.headers['Content-Type'] =  blob.content_type 
        resp.headers['Content-Length'] =  str(blob.size)
        
        resp.headers['Cache-Control'] = 'no-cache'
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Vary'] = 'Origin'


        if( blob.content_type.startswith('image') and thumbnail_enabled == 'True' ):
            resizeCommand = path[1]
            if(resizeCommand==None):
                resizeCommand = ''
                
            return redirect( blob.public_url + resizeCommand ) 
            
        else:
            return blob.download_as_string(), 200
            blob.close()

    
    return 'OK',200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
    
