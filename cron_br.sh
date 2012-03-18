#!/bin/sh
if ps -ef | grep -v grep | grep brit.sh ; then
	exit 0
else
	/home/jono/validation-service/brit.sh &
fi
