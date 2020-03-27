SERVERNAME = cdn.jtn.im
APPENGINE = ../google_appengine
LOCAL_PORT = 8080

install_libs:
	pip install -t lib -r requirements.txt 

run_local_python2:
	dev_appserver.py .

deploy:
	gcloud app deploy

test_remote:
	curl http://$(SERVERNAME)/grand/test

run_local_python3:
	python main.py

log_remote:
	gcloud app logs tail -s default
