#!/bin/bash 

TIME_CLOCK=/home/pi/Desktop/TimeClock.sh
LOCK_FILE=/tmp/time_clock.lock

if test -f "$LOCK_FILE"; then
	PID=$(head -n 1 $LOCK_FILE)
	if ps $PID; then
		echo "Process Running"
		exit
	else
		echo "Attempting to start"
		$TIME_CLOCK	
	fi
else
	$TIME_CLOCK
fi

