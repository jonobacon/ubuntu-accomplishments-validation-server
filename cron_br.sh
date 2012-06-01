#!/bin/sh
if ps -ef | grep -v grep | grep brit.py ; then
	exit 0
else
	python ~/validation-service/brit.py &
fi
