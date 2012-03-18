#!/bin/sh
if ps -ef | grep -v grep | grep workerbatch.py ; then
	exit 0
else
	python /home/jono/validation-service/workerbatch.py &
fi
