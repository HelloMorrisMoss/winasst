import os
import win32com
import subprocess
import time
from datetime import datetime
import win10toast as ts  # this has had it's __init__.py file replaced with the one from
# https://github.com/Charnelx/Windows-10-Toast-Notifications to enable clickable toasts
from typing import Callable
from check_calendar import check_appts_soon
from qlog import qlog
from toaster import get_toasty


# def get_toasty(title: str, message: str, action: Callable = None):
#     """Create a windows 10 toast notification.
#
#     :param title: str
#         toast popup title
#     :param message: str
#         toast popup body text
#     :param action:
#         optional Callable, such as a function, when the toast is clicked
#     :rtype: None
#     """
#     toaster = ts.ToastNotifier()
#     clicked = toaster.show_toast(title,
#                                  message,
#                                  callback_on_click=action)


def check_progs():
    print('{tm} Checking programs.'.format(tm=datetime.now()))

    # what processes are open?
    # universal_newlines=True was NEEDED; caused out of index error on the list after .split() the rows
    output = subprocess.check_output("tasklist.exe", shell=True, universal_newlines=True)
    # print(output)

    # reset processes found
    for key, val in procs_2_watch.items():
        val['running'] = False

    # check the output for the processes
    for rw in output.splitlines():
        rwsplt = rw.split()
        if len(rwsplt) > 0:
            if rwsplt[0] in proc_nms:
                procs_2_watch[rwsplt[0]]['running'] = True
                # print(rwsplt)
    for key, val in procs_2_watch.items():
        # print(key, val)
        if not val['running']:
            print('Trying to open: {}'.format(val['name']))
            # os.popen(['c:\windows\system32\cmd.exe {app}'.format(app=val['cmd']))
            get_toasty('Missing Programs', 'Trying to open: {}'.format(val['name']))

            # TODO: change the below to a function to pass to the get toasty call
            # change to the startin directory then run the command
            command_to_send = 'cd ' + val['startin'] + ' && ' + val['cmd']
            os.popen(command_to_send)
            # print(rwsplt)

            qlog('Tried to open {key}'.format(key=key))
    print('Check complete')


if __name__ == '__main__':
    qlog('Program started.')

    # dictionary of processes to watch
    # if the top level key isn't found in tasklist output then the sub-dictionary is used to try to start the program


    procs_2_watch = {
        'Teams.exe': {
            'name': 'Teams',
            'startin': r'"C:\Users\lmcglaughlin\AppData\Local\Microsoft\Teams"',
            'cmd': r'C:\Users\lmcglaughlin\AppData\Local\Microsoft\Teams\Update.exe --processStart "Teams.exe"',
            'running': False
        },
        'OUTLOOK.EXE': {
            'name': 'Outlook',
            'startin': r'"C:\Program Files\Microsoft Office\root\Office16"',
            'cmd': r'"C:\Program Files\Microsoft Office\root\Office16\OUTLOOK.EXE"',
            'running': False
        },
        'lync.exe': {
            'name': 'Skype',
            'startin': r'"C:\Program Files\Microsoft Office\root\Office16"',
            'cmd': r'"C:\Program Files\Microsoft Office\root\Office16\lync.exe"',
            'running': False
        },
        'googledrivesync.exe': {
            'name': 'gdrive',
            'startin': r'"C:\Program Files\Google\Drive"',
            'cmd': r'"C:\Program Files\Google\Drive\googledrivesync.exe"',
            'running': False
        }
    }

    # process names to look for in tasklist output
    proc_nms = procs_2_watch.keys()

    # program check time
    prog_time = datetime.strptime("1970-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")

    # remind to stretch
    stretch_time = prog_time

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

            # every once in a while remind to stretch
            since_stretch = now - stretch_time
            if since_stretch.seconds > 900:
                get_toasty("Get stretchin'!", 'Stretch and look outside, maybe walk a bit.')
                # qlog('Stretch reminder popup.')
                print('Stretch reminder popup.')
                stretch_time = now

            # check if appts are coming up soon
            since_appts = now - appt_time
            if since_appts.seconds > 300:
                print('Checking for appts.')
                check_appts_soon()
                appt_time = now

            # wait a while before checking again
            time.sleep(10)
    except (KeyboardInterrupt, SystemExit):
        qlog('Assistant program ended by user.')

