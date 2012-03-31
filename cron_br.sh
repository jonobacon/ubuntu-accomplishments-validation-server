#!/bin/sh
if ps -ef | grep -v grep | grep brit.py ; then
	exit 0
else
	python /home/jono/validation-service/brit.py >> /home/jono/logs/brit.log &
fi
