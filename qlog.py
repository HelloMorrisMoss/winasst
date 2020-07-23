from datetime import datetime
def qlog(msg):
    log_here = r"C:\my documents\assistant_log.txt"
    # print(datetime.now())
    with open(log_here, 'a') as lf:
        lf.writelines('{tm} {msg}.\n'.format(tm=datetime.now(), msg=msg))