FROM ubuntu:16.04

MAINTAINER Maxim Pak

# Install required packages and remove the apt packages cache when done.

RUN apt-get update && apt-get install -y \
	git \
	python3 \
	python3-dev \
	python3-setuptools \
#	nginx \
#	supervisor \
#	sqlite3 \
	libmysqlclient-dev \
	build-essential \
	libssl-dev \
	vim
  
RUN apt-get upgrade -y && rm -rf /var/lib/apt/lists/*

# Make 'python' command to point to python3
#RUN alias python=python3

RUN easy_install3 pip

# setup all the configfiles
#RUN echo "daemon off;" >> /etc/nginx/nginx.conf

#COPY nginx.conf /etc/nginx/sites-available/default
#COPY supervisor-app.conf /etc/supervisor/conf.d/supervisor.conf

# COPY requirements.txt and RUN pip install BEFORE adding the rest of your code, this will cause Docker's caching mechanism
# to prevent re-installinig (all your) dependencies when you made a change a line or two in your app.

COPY requirements.txt /home/docker/
RUN pip install -r /home/docker/requirements.txt

RUN ln -s /usr/bin/python3 /usr/bin/python 
# Assuming we always want to run the latest packages
# RUN pip freeze --local | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U

# EXPOSE 80
#CMD ["supervisord", "-n"]
