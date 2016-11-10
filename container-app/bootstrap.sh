#!/bin/sh
# Create directory for uwsgi logs
mkdir -p /var/log/uwsgi
# Create directory for uwsgi config
mkdir -p /etc/uwsgi/vassals/
# Symlink uwsgi config
ln -sf /carparker/container-app/carparker_uwsgi.ini /etc/uwsgi/vassals/carparker_uwsgi.ini

# Create supervisord config
ln -sf /carparker/container-app/supervisor.conf /etc/supervisor/conf.d/supervisor.conf

# Start supervisord process
# supervisord -n 

