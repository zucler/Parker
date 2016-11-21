FROM ubuntu:16.04

MAINTAINER Maxim Pak

# Install required packages and remove the apt packages cache when done.

RUN apt-get update && apt-get install -y \
	git \
	python3 \
	python3-dev \
	python3-setuptools \
	supervisor \
	libmysqlclient-dev \
	build-essential \
	libssl-dev \
	vim \
    net-tools \
    ruby-full \
    rubygems \
    mysql-client \
    netcat \
    fontconfig \
    curl

# Install SASS 
RUN gem install sass

# Install phantomjs
ADD https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2 /home/docker/phantomjs.tar.bz2

RUN cd /home/docker && tar -xjf phantomjs.tar.bz2 && ln -s /home/docker/phantomjs-2.1.1-linux-x86_64/bin/phantomjs /usr/local/bin/phantomjs

# Upgrade all libraries
RUN apt-get upgrade -y && rm -rf /var/lib/apt/lists/*

# Make 'python' command to point to python3
#RUN alias python=python3

RUN easy_install3 pip

# COPY requirements.txt and RUN pip install BEFORE adding the rest of your code, this will cause Docker's caching mechanism
# to prevent re-installinig (all your) dependencies when you made a change a line or two in your app.
COPY requirements.txt /home/docker/
RUN pip install -r /home/docker/requirements.txt

# Create user for uwsgi
RUN useradd -ms /bin/bash uwsgi
RUN usermod -a -G www-data uwsgi
