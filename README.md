#About#

This project expands on the C function tracing methods applied in the other projects and applies similar principles to power management. It is currently in testing mode, where it iterates through various processor clocks and executes runs of various programs. The goal is to be able to execute a program trace, determine the type of program running (i.e. how much speed it needs) and place it onto an appropriately clocked CPU core.



#Project Notes#

-command line tools used:
        bzip2
        grep
        wget
        cpufreq-info
        cpufreq-set
        python3

-all programs must be run as root in the command line
-example:
        ```sudo python3 power_manager_test_bzip2.py```

-frequency settings/steppings will most likely
 have to be adjusted manually due to varying processor types



