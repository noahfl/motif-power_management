#!/usr/bin/python3

"""
Tests fibonacci runs at each processor step; runs
100 times per frequency.

Note: the program grabs the frequency automatically,
but the steps need to be found by running the
command 'cpufreq-info'.

@author: Noah Frazier-Logue (n.frazier.logue@nyu.edu)

"""

from subprocess import Popen, call
import re
import time
import os
import sys

def get_frequency():
    """
    Searches /proc/cpuinfo for frequency using regex
    and returns it as a float.

    @rtype: float
    @return frequency: specified frequency of CPU
    """
    file = open('/proc/cpuinfo', 'r')
    cpuinfo = file.readlines()
    file.close()

    for i in cpuinfo:
        result = re.search("[0-9.]+(GHz)", i)
        if result:
            frequency = result.group()
            print('Frequency: ', frequency)
            frequency = float(frequency.strip('GHz'))
            return frequency

def record_time(file, time, freq, run):
    """
    Records frequency, run number, and time taken for
    each download run and saves them to times.txt.

    @type file: file object
    @param file: opened times.txt file

    @type start_time: float
    @param start_time: start time for given run

    @type freq: string
    @param freq: frequency for given run

    @type run: int
    @param run: number of run
    """
    total_time = time
    total_time = str(round((total_time), 4))
    line = ('Frequency: ' + freq + ' Run: ' + str(run) + ' Time: ' +
               str(total_time) + '\n')
    print(line)
    file.write(line)
    
    
    

def trace_runs(file, freq):
    """
    Decrements from max CPU frequency to 0.9GHz; opens
    fib program, assigns process to core 0, and calls
    record_time to record the time taken

    @type file: file object
    @param file: opened times.txt file

    @type freq: float
    @param freq: frequency for given run
    """
    frequency = freq
    iterator = (4/30)
    min_freq = 1.6
    while (frequency >= min_freq):
	#This all had to be done because
	#cpufreq-set reads frequencies oddly
        #rounded version of frequency
        #frequency = round(frequency, 3)
        freq_str = str(frequency)
        freq_str_test = str("%.2f" % frequency)
        if (list(freq_str_test)[3] == '3'):
            freq_str = "%.2f" % frequency
        # == 'sudo cpufreq-set -c 0 -f [freq]Ghz'
        set_freq = Popen(['sudo', 'cpufreq-set', '-c', '0', '-f',
                          (freq_str + 'Ghz')])
        set_freq.communicate()
        time_sum = 0
        print('Starting at ', freq_str, 'GHz.')
        run_range = 100
        for i in range(run_range):
            start_time = time.time()
            # == 'python3 fib_generator.py'
            proc = Popen(['python3', 'fib_generator.py'])
            pid = str(proc.pid)
            set_core = Popen(['sudo', 'taskset', '-cp', '0', pid])
            set_core.communicate()
            proc.communicate()
            # == 'sudo taskset -cp 0 [pid]'
            print(set_core.pid)
            timer = time.time() - start_time
            time_sum += timer
            record_time(file, timer, freq_str, str(i))
            print('Run ', i, ' done.')
        average = round((time_sum / run_range), 3)
        file.write("Average: " + str(average) + "\n")
        frequency -= iterator

def main():
    """
    Program driver; checks if program is started as
    root and prompts for password if necessary; opens
    times.txt and runs necessary functions.
    """
    euid = os.geteuid()
    if euid != 0:
        print("Script not started as root. Running sudo...")
        args = ['sudo', sys.executable] + sys.argv + [os.environ]
        # the next line replaces the currently-running process with the sudo
        os.execlpe('sudo', *args)
    print('Running. Your euid is', euid)

    file = open('./cpu_output_files/times.txt', 'w+')
    freq = get_frequency()
    trace_runs(file, freq)
    print('Finished.')
    reset_freq = Popen(['sudo', 'cpufreq-set', '-c', '0', '-f',
             (str(freq) + 'Ghz')])
    reset_freq.communicate()
    print("Frequency reset.")

main()

