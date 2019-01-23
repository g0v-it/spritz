FROM tiangolo/uwsgi-nginx-flask:python3.6

MAINTAINER Reinhard Spisser "reinhard@spisser.it"
RUN apt-get update -y
RUN apt-get install -y sqlite3
RUN apt-get install -y libsasl2-dev python-dev libldap2-dev libssl-dev


RUN mkdir -p /opt/voting

RUN mkdir -p /opt/voting/bin
RUN mkdir -p /opt/voting/database
RUN mkdir -p /opt/voting/elections
run mkdir -p /var/www/voting/frontend/web

COPY backend/ /opt/voting/bin
RUN chmod +x /opt/voting/bin/*
COPY requirements.txt /
RUN pip install -r /requirements.txt
WORKDIR /var/www/voting/frontend/web
COPY frontend/ /var/www/voting/frontend/web/
COPY frontend/ /app
COPY frontend/index.py /app/main.py
ARG version
ENV voting_version=$version
VOLUME /opt/voting/database
