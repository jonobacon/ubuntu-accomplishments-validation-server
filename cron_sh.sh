#!/bin/sh
if ps -ef | grep -v grep | grep shares.py ; then
	exit 0
else
	/home/jono/validation-service/process-shares &
fi
