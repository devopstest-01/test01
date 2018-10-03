FROM ubuntu:18.04
FROM python:2.7

RUN apt-get update -y && apt-get install -y curl

COPY local /code

WORKDIR /code

RUN pip2.7 install -r requirements.txt

CMD [ "uwsgi", "--http", "0.0.0.0:5000", \
               "--uid", "www-data", "--enable-threads", \
               "--plugins", "python2.7", \
               "--protocol", "uwsgi", \
               "--wsgi", "wsgi:webapp", \
	       "--master", "--processes", "4", "--threads", "2" ]

