import os
import psutil
import sys

TIME_CLOCK = "/tmp/time_clock.lock"


def apply_lock():
    with open(TIME_CLOCK, 'w') as file:
        pid = str(os.getpid())
        file.write(pid)


def session_lock_check():
    if os.path.exists(TIME_CLOCK):
        with open(TIME_CLOCK, 'r') as lock_file:
            lock_file_pid = lock_file.readline()
        if lock_file_pid in psutil.pids():
            # The process is running, kill this one
            sys.exit("process is already running")
        else:
            apply_lock()
    else:
        apply_lock()
