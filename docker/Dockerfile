FROM ubuntu
MAINTAINER Abner

ENV DFXK_CMDB_REPO_URL https://gitlab.dfxkdata.com/devops/dfxk-cmdb.git

COPY ./source.list /etc/apt/source.list

RUN apt-get update
RUN apt-get install -y wget
RUN apt-get install -y git
RUN apt-get install -y vim

RUN apt-get update
RUN apt-get install -y python3-pip
RUN apt-get install -y python3-dev
RUN apt-get -y install build-essential libssl-dev libffi-dev
COPY ./requiement.txt /tmp/requiement.txt
RUN pip3 install -r /tmp/requiement.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
RUN apt-get -y clean
RUN apt-get -q -y autoremove

RUN mkdir /opt
RUN cd /opt && git clone $DFXK_CMDB_REPO_URL
WORKDIR /opt/dfxk-cmdb

EXPOSE 8000

CMD ["/bin/bash", "-c", "python3 manage.py runserver 0.0.0.0:8000"]

