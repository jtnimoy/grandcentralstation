SERVERNAME = cdn.jtn.im
APPENGINE = ../google_appengine
LOCAL_PORT = 8080


local_server:
	$(APPENGINE)/dev_appserver.py .

deploy:
	$(APPENGINE)/appcfg.py update .

test_remote:
	curl http://$(SERVERNAME)/grand/test

test_local:
	curl http://localhost:$(LOCAL_PORT)/grand/test

