 grandcentralstation
===================

static file server for google app engine that serves from of google cloud storage, bypassing the "Make Public" checkbox feature. Already supports dynamic image resizing (server side thumbnail generation)

## Name Meaning ##
GrandCentralStation is a backronym on the initials of Google Cloud Storage.

![https://github.com/jtnimoy/grandcentralstation/blob/master/data/gcs-logo.jpg]

## Project Goals ##
Maintain a lightweight, static file server that provides more flexible features beyond the simple "make public" checkbox currently found in Google Cloud Storage. To add some popular features from more robust web servers like Apache and nginx, approaching  a comfortable middle ground.

## Backstory ##
I needed more control than turnkey solutions would provide when migrating my 16 year old web portfolio into the cloud era. I knew I needed to have the files come from a CDN, and needed as much flexibility as I could make possible for future antics. Cloudflare Mirage seemed too hands-off, and Bitnami's Gallery had way too much front-end. Having a headache on AWS writing my own static file server for S3 that also cached thumbnails, I decided to give google cloud storage + google app engine a go. It has so far turned out to be a much smoother experience and I think I'll stay on the Google Cloud.

## Installation ##

+ You need to have [Google App Engine SDK](https://developers.google.com/appengine) for Python.

+ clone or download the grandcentralstation folder and add it as an app engine project. Change the value of `application` in app.yaml to reflect your project's name.

+ Make sure your GAE project has Google Cloud Storage service added, and upload some files to it.

+ Download and install the [Cloud Storage Client Library](https://developers.google.com/appengine/docs/python/googlecloudstorageclient/download) into your project.

+ grandcentralstation will use your default bucket name (the one created for you which is the same name as your project). Deploy the app to appspot, and insure that you are able to access one of your bucket files at that domain. For example, if the bucket file is `gs://cdn.jtn.im/poodles/duncan.jpg` then the URL will be `http://myproject.appspot.com/poodles/duncan.jpg`.

+ Images have a dynamic resizing feature in accordance with the app engine image api. Append `=s100` to the end of an image URL to see the longest length resized to 100. To enable cropping and have the image returned as a 100x100 square, append `-s100-c`.

