"""Control the system volume and mute state."""


from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, ISimpleAudioVolume
import argparse
from math import log


class Volume:
    def __init__(self):
        self.devices = AudioUtilities.GetSpeakers()
        self.interface = self.devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(self.interface, POINTER(IAudioEndpointVolume))

    def mute(self):
        """Mute the system volume."""
        self.volume.SetMute(1, None)


    def unmute(self):
        """Unmute the system volume."""
        self.volume.SetMute(0, None)


if __name__ == '__main__':
    sessions = AudioUtilities.GetAllSessions()
    for ses in sessions:
        vol = ses._ctl.QueryInterface(ISimpleAudioVolume)


