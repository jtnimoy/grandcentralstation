SERVERNAME = cdn.jtn.im
APPENGINE = ../google_appengine
LOCAL_PORT = 8080


local_server:
	dev_appserver.py .

deploy:
	gcloud app deploy

test_remote:
	curl http://$(SERVERNAME)/grand/test

test_local:
	curl http://localhost:$(LOCAL_PORT)/grand/test

