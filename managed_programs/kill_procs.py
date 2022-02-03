from data_dicts import procs_2_watch
import os


def kill_by_name(kill_name):
    os.system(f"taskkill /F /im {kill_name}")


if __name__ == '__main__':
    for k, v in procs_2_watch.items():
            try:
                for proc in v['kill_list']:
                        kill_by_name(proc)
            except KeyError:
                kill_by_name(k)
