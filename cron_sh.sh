#!/bin/sh
if ps -ef | grep -v grep | grep sharecheck.py ; then
	exit 0
else
	/home/jono/validation-service/process-sharecheck >> /home/jono/logs/shares.log &
fi
