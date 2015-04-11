#!/bin/bash

PIDFILE=/var/run/securitycam.pid
PID=$(<$PIDFILE)
PID_COUNT=$(ps -eo pid|grep -c $PID)
echo $PID_COUNT
exit 0
