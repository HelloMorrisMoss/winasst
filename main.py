import os
import random
import subprocess
import time
from datetime import datetime

from managed_programs.data_dicts import procs_2_watch
# https://github.com/Charnelx/Windows-10-Toast-Notifications to enable clickable toasts
from gui import SettingsWindow
from qlog import lg
from system.toaster import get_toasty
# an attempt to avoid having time.sleep in the loop below, removing them CPU went to 20-30%
# this is to set to use only 1 CPU core, it didn't help
# import os
# os.environ["OPENBLAS_NUM_THREADS"] = "1"
# os.environ["MKL_NUM_THREADS"] = "1"
from noise_makers.voice import read_this


def open_that(key, val):
    # TODO: change the below to a function to pass to the get toasty call
    # change to the startin directory then run the command
    command_to_send = 'cd ' + val['startin'] + ' && ' + val['cmd']
    os.popen(command_to_send)
    # lg.info(rwsplt)
    lg.info('Tried to open {key}'.format(key=key))


def check_progs(settings_dict, open_all=False):
    lg.info('{tm} Checking programs.'.format(tm=datetime.now()))

    # what processes are open?
    # universal_newlines=True was NEEDED; caused out of index error on the list after .split() the rows
    output = subprocess.check_output("tasklist.exe", shell=True, universal_newlines=True)
    # lg.info(output)

    # reset processes found
    for key, val in procs_2_watch.items():
        val['running'] = False if settings_dict[key] else True

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
            if open_all:
                open_that(key, val)
            else:
                lg.info('{} is not open, prompting to open.'.format(val['name']))
                # os.popen(['c:\windows\system32\cmd.exe {app}'.format(app=val['cmd']))
                get_toasty('Missing Programs', 'Click to try to open: {}'.format(val['name']), open_that, key, val)

    lg.info('Check complete')


def background_process(settings_dict, **kwargs):
    # global prog_time, first_run, stretch_time
    # program check time
    prog_time = datetime.strptime("1970-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
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
            # since_appts = now - appt_time
            # if since_appts.seconds > 300:
            #     lg.info('Checking for appts.')
            #     check_appts_soon()
            #     appt_time = now
            #     lg.info('Appts check complete.')

            # wait a while before checking again
            lg.info('Sleep for 60s')
            time.sleep(60)
            lg.info('end sleep')
    except (KeyboardInterrupt, SystemExit):
        lg.info('Assistant program ended by user.')


if __name__ == '__main__':
    lg.info('Program started.')

    # process names to look for in tasklist output
    proc_nms = procs_2_watch.keys()

    stretch_attention_prefixes = [
        'hey is for horses, stretching is for backs {}', 'yoyos go up and down, backs go round and round, {}',
        'hello there general {}', 'salutations, some back, terrific, radiant, {}',
        'hey you, the one with the back, {}',
        'you know, you better {}', 'yo there stretch {}', 'hey mambo, mambo  {},' 'holla at yo back, {}',
        'onomatopoeia, you know I wannna see ya, {}', 'wahmbology, the study of  {}',
        'interesting, did you know you should {}', 'we place stretching before everything else',
        'it says here that you need to {}',
        'here yee here yee, the time has commeth to {}', 'wibbly wobbly time-ee wimey to {}',
        'look its count back-ula, {}', 'rule number one of chair-zombie land is {}',
        'you know you are going to have to need to {}', 'back streets back all right, {}',
        'henceforth this shall be known as the time whence it was time to {}',
        'roll a stretching check {}', 'fetch the retch to etch the ketchup catch and {}',
        'watch behind you, your back is getting sore {}',
        "you know it's wack if you jack your back while piling the stack, {}",
        "Put your hand on your hips, yee-aiyuh. Let your backbone slip. Do the Watusi. Stretch your back real loosey.",
        'the secret ingredient is to {}', 'did I ever tell you about the time you need to {}',
        "text-to-speech bots don't have backs, if I had a back like you, you know I would {}",
        "Mrs. Frisbee and the backs of NIMH, {}", "wickety wickety wack, it's time to stretch your back",
        "Hey, what's that out the window, now would be a great time to {}",
        "Who was that behind you? Could it be time to {} already?", "How did it get so late, it's already time to {}!",
        "I want to tell you something, {}!", "Can you still kick yourself in the back of the head? {}",
        "Ha. Ha. Ha. It's so funny I almost forgot to {}", "Wet Fetching. Let Retching. Get stretching.",
        "Some body once told me. The world is gonna roll me. I ain't the stetch-est back in the shed!",
        "Roll for initiative. {}!", "Give me a con save vs sore back. {}!",
        "The wizard casts elastic back. Get stretching.", "Are you ignoring me? {}"
    ]

    # whether the loop has run once or not
    first_run = True
    # TODO: on first run try to connect to corporate network: something like: netsh wlan connect "NA-LW Corporate"

    # loop through processes every once in a while to check for programs which frequently give trouble about being open
    settings_d = {key: False for key in procs_2_watch.keys()}
    SettingsWindow(background_process, settings_d)
    background_process()

# hung trying to toast popup
# 2020-11-06 13:00:35,665        main.<module>.112                             DEBUG: Stretch reminder popup starting.
