#!/bin/sh
if ps -ef | grep -v grep | grep process-shares ; then
	exit 0
else
	/home/jono/validation-service/process-shares >> /home/jono/logs/process-shares.log &
fi
