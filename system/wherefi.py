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
    tasklist = subprocess.check_output('tasklist', shell=True, universal_newlines=True)
    print(tasklist)
    if "NetClient.exe" in tasklist:
        lg.debug('VPN work')
        at_work = True

    # if we haven't found anything, not at work
    return at_work


if __name__ == '__main__':
    # print(work_net())
    # import scapy
    # from scapy.all import *
    # # from scapy.layers import Dot11
    # #
    # # ap_list = []
    # #
    # #
    # # def PacketHandler(pkt):
    # #
    # #     if pkt.haslayer(Dot11):
    # #         if pkt.type == 0 and pkt.subtype == 8:
    # #             if pkt.addr2 not in ap_list:
    # #                 ap_list.append(pkt.addr2)
    # #                 print
    # #                 "AP MAC: %s with SSID: %s " % (pkt.addr2, pkt.info)
    # #
    # #
    # # sniff(iface="mon0", prn=PacketHandler)
    # sniff(iface="Wi-Fi", monitor=True, prn=lambda x:x.sprintf("{Dot11Beacon:%Dot11.addr3%\t%Dot11Beacon.info%\t%PrismHeader.channel%\t%Dot11Beacon.cap%}"))

    print(work_net())