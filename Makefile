SERVERNAME = cdn.jtn.im
APPENGINE = ../google_appengine
LOCAL_PORT = 8080


local_server:
	dev_appserver.py .

deploy:
	rm *.pyc; rm -r __pycache__ ; gcloud app deploy

test_remote:
	curl http://$(SERVERNAME)/grand/test

test_local:
	curl http://localhost:$(LOCAL_PORT)/grand/test

log_remote:
	gcloud app logs tail -s default
