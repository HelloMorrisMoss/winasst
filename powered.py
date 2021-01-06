# Get power status of the system using ctypes to call GetSystemPowerStatus
# thanks to https://stackoverflow.com/a/6156606

import ctypes
from ctypes import wintypes


class SYSTEM_POWER_STATUS(ctypes.Structure):
    _fields_ = [
        ('ACLineStatus', wintypes.BYTE),
        ('BatteryFlag', wintypes.BYTE),
        ('BatteryLifePercent', wintypes.BYTE),
        ('Reserved1', wintypes.BYTE),
        ('BatteryLifeTime', wintypes.DWORD),
        ('BatteryFullLifeTime', wintypes.DWORD),
    ]

    def is_plugged(self):
        return self.ACLineStatus == 1


def power_info():
    SYSTEM_POWER_STATUS_P = ctypes.POINTER(SYSTEM_POWER_STATUS)

    GetSystemPowerStatus = ctypes.windll.kernel32.GetSystemPowerStatus
    GetSystemPowerStatus.argtypes = [SYSTEM_POWER_STATUS_P]
    GetSystemPowerStatus.restype = wintypes.BOOL

    status = SYSTEM_POWER_STATUS()
    if not GetSystemPowerStatus(ctypes.pointer(status)):
        raise ctypes.WinError()
    return status
    # print('ACLineStatus', status.ACLineStatus)
    # print('BatteryFlag', status.BatteryFlag)
    # print('BatteryLifePercent', status.BatteryLifePercent)
    # print('BatteryLifeTime', status.BatteryLifeTime)
    # print('BatteryFullLifeTime', status.BatteryFullLifeTime)


if __name__ == '__main__':
    power_status = power_info()
    print(power_status.ACLineStatus)
    print(power_status.is_plugged())
