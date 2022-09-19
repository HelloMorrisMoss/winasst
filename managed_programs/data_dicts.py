from collections import OrderedDict

# dictionary of processes to watch

# if the top level key isn't found in tasklist output then the sub-dictionary is used to try to start the program

procs_2_watch = OrderedDict()

procs_2_watch['OUTLOOK.EXE'] = {
    'name': 'Outlook',
    'startin': r'"C:\Program Files\Microsoft Office\root\Office16"',
    'cmd': r'"C:\Program Files\Microsoft Office\root\Office16\OUTLOOK.EXE"',
    'running_val': False,
    'pop_up': True,
    'voice_alert': False,
    'voice_message': 'Outlook is not running.',
    'initial_start': True,
    }
procs_2_watch['Teams.exe'] = {
    'name': 'Teams',
    'startin': r'"C:\Users\lmcglaughlin\AppData\Local\Microsoft\Teams"',
    'cmd': r'C:\Users\lmcglaughlin\AppData\Local\Microsoft\Teams\Update.exe --processStart "Teams.exe"',
    'running_val': False,
    'pop_up': True,
    'voice_alert': False,
    'voice_message': 'Teams is not running.',
    'initial_start': False,
    }
# procs_2_watch['lync.exe'] = {
#     'name': 'Skype',
#     'startin': r'"C:\Program Files\Microsoft Office\root\Office16"',
#     'cmd': r'"C:\Program Files\Microsoft Office\root\Office16\lync.exe"',
#     'running_val': False
# }
procs_2_watch['googledrivesync.exe'] = {
    'name': 'gdrive',
    'startin': r'"C:\Program Files\Google\Drive"',
    'cmd': r'"C:\Program Files\Google\Drive\googledrivesync.exe"',
    'running_val': False,
    'pop_up': True,
    'voice_alert': False,
    'voice_message': 'G drive is not running.',
    'initial_start': False,
    }

procs_2_watch['aw-server.exe'] = {
    'name': 'ActivityWatch',
    'startin': r'"C:\Users\lmcglaughlin\AppData\Local\Programs\ActivityWatch"',
    'cmd': r'"C:\Users\lmcglaughlin\AppData\Local\Programs\ActivityWatch\aw-qt.exe"',
    'running_val': False,
    'pop_up': True,
    'voice_alert': False,
    'voice_message': 'Activity Watch is not running.',
    'kill_list': ['aw-server.exe', 'aw-qt.exe', 'aw-watcher-window.exe', 'aw-watcher-afk.exe'],
    'initial_start': True,
    }
