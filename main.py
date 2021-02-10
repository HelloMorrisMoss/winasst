import os
import win32com
import subprocess
import time
from datetime import datetime
import random
import win10toast as ts  # this has had it's __init__.py file replaced with the one from
# https://github.com/Charnelx/Windows-10-Toast-Notifications to enable clickable toasts
from typing import Callable
from check_calendar import check_appts_soon
from qlog import lg
from toaster import get_toasty
from collections import OrderedDict

# an attempt to avoid having time.sleep in the loop below, removing them CPU went to 20-30%
# this is to set to use only 1 CPU core, it didn't help
# import os
# os.environ["OPENBLAS_NUM_THREADS"] = "1"
# os.environ["MKL_NUM_THREADS"] = "1"
from voice import read_this
from data_dicts import procs_2_watch


def open_that(key, val):
    # TODO: change the below to a function to pass to the get toasty call
    # change to the startin directory then run the command
    command_to_send = 'cd ' + val['startin'] + ' && ' + val['cmd']
    os.popen(command_to_send)
    # lg.info(rwsplt)
    lg.info('Tried to open {key}'.format(key=key))


def check_progs():
    lg.info('{tm} Checking programs.'.format(tm=datetime.now()))

    # what processes are open?
    # universal_newlines=True was NEEDED; caused out of index error on the list after .split() the rows
    output = subprocess.check_output("tasklist.exe", shell=True, universal_newlines=True)
    # lg.info(output)

    # reset processes found
    for key, val in procs_2_watch.items():
        val['running'] = False

    # check the output for the processes
    for rw in output.splitlines():
        rwsplt = rw.split()
        if len(rwsplt) > 0:
            if rwsplt[0] in proc_nms:
                procs_2_watch[rwsplt[0]]['running'] = True
                # lg.info(rwsplt)
    for key, val in procs_2_watch.items():
        # lg.info(key, val)
        if not val['running']:
            lg.info('{} is not open, prompting to open.'.format(val['name']))
            # os.popen(['c:\windows\system32\cmd.exe {app}'.format(app=val['cmd']))
            get_toasty('Missing Programs', 'Click to try to open: {}'.format(val['name']), open_that, key, val)

    lg.info('Check complete')


if __name__ == '__main__':
    lg.info('Program started.')
    
    # process names to look for in tasklist output
    proc_nms = procs_2_watch.keys()

    # program check time
    prog_time = datetime.strptime("1970-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")

    # remind to stretch
    stretch_time = prog_time
    stretch_attention_prefixes = ['hey', 'yo', 'hello', 'good day', 'salutations', 'hey you', 'you better', 'yo stretch',
                                  'hey mambo,' 'holla at yo back,', 'onomatopoeia', 'wombo', 'interesting',
                                  'we place stretching before everything else', 'it says here that you need to',
                                  'here yee here yee, the time has commeth to', 'wibbly wobbly time-y wimey to',
                                  'look its count back-ula,', 'rule number one of chair-zombie land is',
                                  'you know you are going to', 'back streets back all right',
                                  'henceforth this shall be known as the time whence it was time to',
                                  'roll a stretching check', 'fetch the retch to etch the ketchup catch and',
                                  'watch behind you, your back is getting sore']

    # appointments check time
    appt_time = prog_time

    # loop through processes every once in a while to check for programs which frequently give trouble about being open
    try:
        while True:
            now = datetime.now()

            # check for programs missing
            since_check = now - prog_time
            if since_check.seconds > 360:
                check_progs()
                prog_time = now
                lg.info('Exited check_progs.')

            # every once in a while remind to stretch
            since_stretch = now - stretch_time
            if since_stretch.seconds > 600:
                lg.info('Stretch reminder popup starting.')
                # get_toasty("Get stretchin'!", 'Stretch and look outside, maybe walk a bit.')
                stretch_prefx = stretch_attention_prefixes[random.randint(0, len(stretch_attention_prefixes) - 1)]
                read_this(f'{stretch_prefx} Get stretching!')
                # qlog('Stretch reminder popup.')
                stretch_time = now
                lg.info('Stretch reminder popup completed.')

            # this seems to cause the assistant to hang with some regularity, disabling for now
            # the hanging still happened without this
            # check if appts are coming up soon
            # since_appts = now - appt_time
            # if since_appts.seconds > 300:
            #     lg.info('Checking for appts.')
            #     check_appts_soon()
            #     appt_time = now
            #     lg.info('Appts check complete.')

            # wait a while before checking again
            lg.info('Sleep for 60s') #, end='')
            time.sleep(60)
            lg.info('end sleep')
    except (KeyboardInterrupt, SystemExit):
        lg.info('Assistant program ended by user.')

# hung trying to toast popup
# 2020-11-06 13:00:35,665        main.<module>.112                             DEBUG: Stretch reminder popup starting.
