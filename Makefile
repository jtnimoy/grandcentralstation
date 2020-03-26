SERVERNAME = cdn.jtn.im
APPENGINE = ../google_appengine
LOCAL_PORT = 8080

install_libs:
	pip install -t lib -r requirements.txt 

local_server:
	dev_appserver.py .

deploy:
	gcloud app deploy

test_remote:
	curl http://$(SERVERNAME)/grand/test

test_local:
	curl http://localhost:$(LOCAL_PORT)/grand/test

log_remote:
	gcloud app logs tail -s default
