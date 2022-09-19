import argparse

from qlog import lg
from system_interface.wherefi import work_net
from system_interface.system_volume import Volume


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--volume', help='Volume to set the system.', type=int)
    parser.add_argument('--mute', help='Mute system audio.', action='store_true')
    parser.add_argument('--unmute', help='Unmute system audio.', action='store_true')
    parser.add_argument('--work', help='Whether to run commands only if at work.', action='store_true')

    args = parser.parse_args()

    # check if at work
    if (args.work and work_net()) or not args.work:
        lg.debug('work check passed')
        vol = Volume()
        if args.mute:
            vol.mute()
        elif args.unmute:
            vol.unmute()
        # elif args.volume:
        #     volume.SetMas(args.volume)
