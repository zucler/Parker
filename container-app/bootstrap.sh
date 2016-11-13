#!/bin/sh
# Create directory for uwsgi logs
mkdir -p /var/log/uwsgi
# Create directory for uwsgi config
mkdir -p /etc/uwsgi/vassals/
# Symlink uwsgi config
ln -sf /carparker/container-app/carparker_uwsgi.ini /etc/uwsgi/vassals/carparker_uwsgi.ini

# Create supervisord config
ln -sf /carparker/container-app/supervisor.conf /etc/supervisor/conf.d/supervisor.conf

# Waiting for MySQL container to start
WAIT=0
while ! nc -z parker-db 3306; do
    sleep 1
    WAIT=$(($WAIT +1))
    if ["$WAIT" -gt 15]; then
        echo "Error: Timeout waiting for db to start"
        exit 1
    fi
done

# import mysql data
find /carparker/db_dump/latest -name '*.sql' | awk '{ print "source",$0 }' | mysql --batch -hparker-db -uroot -proot parker 

# Start supervisord process
supervisord -n 

