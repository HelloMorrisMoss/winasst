from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import argparse

from wherefi import work_net

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))


def mute():
    volume.SetMute(1, None)


def unmute():
    volume.SetMute(0, None)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mute', help='Mute system audio.', action='store_true')
    parser.add_argument('--unmute', help='Unmute system audio.', action='store_true')

    args = parser.parse_args()

    # check if at work
    if work_net():

        if args.mute:
            mute()
        else:
            unmute()

