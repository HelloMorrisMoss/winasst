"""Check where the PC is being used based on which WIFI/ethernet is connected."""

import subprocess
from qlog import lg

# # universal_newlines=True was NEEDED; caused out of index error on the list after .split() the rows
# output = subprocess.check_output("netsh wlan show interfaces", shell=True, universal_newlines=True)
# print(output)
# if "NA-LW Corporate" in output:
#     print('work')


def work_net():
    """Check if connected to work wifi/ethernet. If so, returns true."""
    # default
    at_work = False

    # check ipconfig for the DNS name
    ipconfig = subprocess.check_output("ipconfig", shell=True, universal_newlines=True)
    print(ipconfig)
    if "LW.permacel.com" in ipconfig:
        lg.debug('work')
        at_work = True

    # check tasklist for the VPN program
    tasklist = subprocess.check_output("tasklist", shell=True, universal_newlines=True)
    if "NetClient" in tasklist:
        at_work = True

    # if we haven't found anything, not at work
    return at_work


