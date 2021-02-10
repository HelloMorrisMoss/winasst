from data_dicts import procs_2_watch
import os

if __name__ == '__main__':
    for k, v in procs_2_watch.items():

        os.system(f"taskkill /F /im {k}")
