grandcentralstation
===================

static file server for google app engine that serves from of google cloud storage, bypassing the "Make Public" checkbox feature. Already supports dynamic image resizing (server side thumbnail generation)

##Name Meaning
GrandCentralStation is a backronym on the initials of Google Cloud Storage.

##Project Goals
Maintain a lightweight, static file server that provides more flexible features beyond the simple "make public" checkbox currently found in Google Cloud Storage.

##Backstory
I needed more control than turnkey solutions would provide when migrating my 16 year old web portfolio into the cloud era. I knew I needed to have the files come from a CDN, and needed as much flexibility as I could make possible for future antics. Cloudflare Mirage seemed too hands-off, and Bitnami's Gallery had way too much front-end. Having a headache on AWS writing my own static file server for S3 that also cached thumbnails, I decided to give google cloud storage + google app engine a go. It has so far turned out to be a much smoother experience and I think I'll stay on the Google Cloud.


