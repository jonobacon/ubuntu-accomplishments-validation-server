#!/bin/sh
if ps -ef | grep -v grep | grep sharecheck.py ; then
	exit 0
else
	~/validation-service/process-sharecheck &
fi
