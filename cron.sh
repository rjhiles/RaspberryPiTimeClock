#!/bin/bash 

export DISPLAY=:0
TIME_CLOCK=/home/pi/Desktop/TimeClock.sh
LOCK_FILE=/tmp/time_clock.lock

if test -f "$LOCK_FILE"; then
	PID=$(head -n 1 $LOCK_FILE)
	if ps $PID; then
		echo "Process Running"
		exit
	else
		echo "Attempting to start"
		/home/pi/Desktop/TimeClock.sh >/dev/null </dev/null		
	fi
else
	/home/pi/Desktop/TimeClock.sh >/dev/null </dev/null
fi

