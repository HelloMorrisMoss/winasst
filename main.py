import argparse
import os
import random
import subprocess
import sys
import time
from datetime import datetime

from check_calendar import check_appts_soon
from config.stretch_prefixes import stretch_attention_prefixes
from managed_programs.data_dicts import procs_2_watch
# https://github.com/Charnelx/Windows-10-Toast-Notifications to enable clickable toasts
from gui import SettingsWindow
from qlog import lg
from system_interface.toaster import get_toasty
# an attempt to avoid having time.sleep in the loop below, removing them CPU went to 20-30%
# this is to set to use only 1 CPU core, it didn't help
# import os
# os.environ["OPENBLAS_NUM_THREADS"] = "1"
# os.environ["MKL_NUM_THREADS"] = "1"
from sound_i0.voice import read_this
from system_interface.wherefi import work_net


def open_that(key, val):
    # TODO: change the below to a function to pass to the get toasty call
    # change to the startin directory then run the command
    command_to_send = 'cd ' + val['startin'] + ' && ' + val['cmd']
    os.popen(command_to_send)
    # lg.info(rwsplt)
    lg.info('Tried to open {key}'.format(key=key))


def check_progs(settings_dict, first_run=False):
    lg.info('{tm} Checking programs.'.format(tm=datetime.now()))

    # what processes are open?
    # universal_newlines=True was NEEDED; caused out of index error on the list after .split() the rows
    output = subprocess.check_output("tasklist.exe", shell=True, universal_newlines=True)
    # lg.info(output)

    # reset processes found
    for key, val in procs_2_watch.items():
        val['running_val'] = False if settings_dict[key] else True

    # check the output for the processes
    for rw in output.splitlines():
        rwsplt = rw.split()
        if len(rwsplt) > 0:
            if rwsplt[0] in proc_nms:
                procs_2_watch[rwsplt[0]]['running_val'] = True
                # lg.info(rwsplt)
    for key, val in procs_2_watch.items():
        # lg.info(key, val)
        if not val['running_val']:
            if first_run:
                if val.get('initial_start'):  # if this one should be started initially
                    open_that(key, val)
            else:
                lg.info('{} is not open, prompting to open.'.format(val['name']))
                get_toasty('Missing Programs', 'Click to try to open: {}'.format(val['name']), open_that, key, val)

    lg.info('Check complete')


def background_process(settings_dict, **kwargs):
    # global prog_time, first_run, stretch_time
    # program check time
    prog_time = datetime.strptime("1970-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
    appt_time = prog_time
    # remind to stretch
    stretch_time = prog_time

    first_run = True
    try:
        while True:
            now = datetime.now()

            # check for programs missing
            since_check = now - prog_time
            if since_check.seconds > 360:
                check_progs(settings_dict, first_run)
                prog_time = now
                lg.info('Exited check_progs.')
                first_run = False

            # every once in a while remind to stretch
            since_stretch = now - stretch_time
            if since_stretch.seconds > 750:
                lg.info('Stretch reminder popup starting.')
                # get_toasty("Get stretchin'!", 'Stretch and look outside, maybe walk a bit.')
                stretch_prefx = stretch_attention_prefixes[random.randint(0, len(stretch_attention_prefixes) - 1)]
                read_this(stretch_prefx.replace('{}', ' Get stretching!'))
                # qlog('Stretch reminder popup.')
                stretch_time = now
                lg.info('Stretch reminder popup completed.')

            # this seems to cause the assistant to hang with some regularity, disabling for now
            # the hanging still happened without this
            # check if appts are coming up soon
            since_appts = now - appt_time
            if since_appts.seconds > 300:
                lg.info('Checking for appts.')
                check_appts_soon()
                appt_time = now
                lg.info('Appts check complete.')

            # wait a while before checking again
            lg.info('Sleep for 60s')
            time.sleep(60)
            lg.info('end sleep')
    except (KeyboardInterrupt, SystemExit):
        lg.info('Assistant program ended by user.')


if __name__ == '__main__':
    lg.info('Program started.')
    cl_parser = argparse.ArgumentParser()
    cl_parser.add_argument('--work_check', help='Check if connected to work network and stop program if not.',
                           action='store_true')
    cl_args = cl_parser.parse_args()

    if cl_args.work_check:
        at_work = work_net()

        if not at_work:
            sys.exit()  # if not connected to the work network, likely don't need to be running
        else:
            lg.info('at work!')

    # process names to look for in tasklist output
    proc_nms: tuple = procs_2_watch.keys()

    # loop through processes every once in a while to check for programs which frequently give trouble about being open
    settings_d = {key: False for key in procs_2_watch.keys()}
    SettingsWindow(background_process, settings_d)

# hung trying to toast popup
# 2020-11-06 13:00:35,665        main.<module>.112                             DEBUG: Stretch reminder popup starting.
