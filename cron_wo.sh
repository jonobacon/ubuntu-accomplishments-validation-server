#!/bin/sh
if ps -ef | grep -v grep | grep worker.sh ; then
	exit 0
else
	/home/jono/validation-service/worker.sh >> /home/jono/logs/worker.log &
fi
