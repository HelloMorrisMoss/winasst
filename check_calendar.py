from inspect import currentframe, getframeinfo
import win32com.client
from datetime import datetime, timezone, timedelta
from traceback import format_exc as exc

# from main import get_toasty
import re
# from dateutil.relativedelta import relativedelta
import win10toast as ts  # this has had it's __init__.py file replaced with the one from
# https://github.com/Charnelx/Windows-10-Toast-Notifications to enable clickable toasts
from typing import Callable
from qlog import qlog


def nowa():
    """Get a local timezone aware datetime for now."""
    # painful to work with dates
    # https://stackoverflow.com/a/25887393/10941169
    utc_dt = datetime.now(timezone.utc)  # UTC time
    dt = utc_dt.astimezone()
    return dt


def get_toasty(title: str, message: str, action: Callable = None):
    toaster = ts.ToastNotifier()
    clicked = toaster.show_toast(title,
                                 message,
                                 callback_on_click=action)


def get_appts():
    """Get appointments from outlook calendar."""
    # https://stackoverflow.com/questions/21477599/read-outlook-events-via-python
    print(getframeinfo(currentframe()).lineno)
    Outlook = win32com.client.Dispatch("Outlook.Application")

    try:
        print(getframeinfo(currentframe()).lineno)
        ns = Outlook.GetNamespace("MAPI")

        appointments = ns.GetDefaultFolder(9).Items
    except AttributeError:
        print(exc())
        appointments = []

    # finally:
    #     Outlook.Quit() # this seems to be closing the existing outlook

    # filtering using Restrict doesn't seem to work properly, it'd probably be faster, but just going to return all of
    # them and filter them after the fact

    # # Restrict to items in the next 30 days (using Python 3.3 - might be slightly different for 2.7)
    # begin = datetime.today() - timedelta(days=1)
    # end = datetime.today() + timedelta(days=1)  # begin + datetime.timedelta(days = 30);
    # # begin = datetime(year=nowa().year, month=nowa().month, day=1)
    # # next_month = begin + timedelta(days=35)
    # # end = datetime(next_month.year, next_month.month, 1)
    #
    # # [Start] >= '07/22/2020 12:00 AM' AND [End] <= '08/21/2020 12:00 AM'
    # # [Start] >= '07/22/2020 12:00 AM'
    #
    # print('begin {} end {}'.format(begin, end))
    # # restriction = "[Start] >= '" + begin.strftime("%m/%d/%Y") + "' AND [End] <= '" + end.strftime("%m/%d/%Y") + "'"
    # # restriction1 = "[Start] >= '" + begin.strftime("%m/%d/%Y 12:00 AM") + "'"
    # # restriction2 = "'[Start] <= '" + end.strftime("%m/%d/%Y 00:00 AM") + "'"
    # # print('restriction1', restriction1)
    # # print('restriction2', restriction2)
    #
    # # str_restriction = "[Start] >= '" + Outlook.Format(begin, "mm/dd/yyyy hh:mm AMPM") + "' AND [End] <= '" & + Outlook.Format(end, "mm/dd/yyyy hh:mm AMPM") & "'"
    # # str_restriction = "[Start] >= '07/22/2020 12:00 AM' AND [End] <= '08/21/2020 12:00 AM'"
    # str_restriction = "[Start]>='07-22-2020 12:00 AM'"
    # restricted_items = appointments.Restrict(str_restriction)
    #
    # # restricted_items = appointments.Restrict(restriction1)
    # # restricted_items = restricted_items.Restrict(restriction2)
    # return restricted_items
    return appointments

# # nevermind, wasn't paying attention, it has .subject, .start etc
# def split_appts(appts):
#     ptrn = re.compile(r'Start:|End:|Organizer')
#     split_appts = []
#     for appt in appts:
#         split_appts.append(re.split(ptrn, appt))
#     print(split_appts)

# restrictedItems = get_appts()
# # Iterate through restricted AppointmentItems and print them
# for appointmentItem in restrictedItems:
#     print("{0} Start: {1}, End: {2}, Organizer: {3}".format(
#           appointmentItem.Subject, appointmentItem.Start,
#           appointmentItem.End, appointmentItem.Organizer))


def check_appts_soon():
    # tz = timezone.tz
    print(getframeinfo(currentframe()).lineno)

    # timezone
    appts = get_appts()
    # now = datetime.now().astimezone(timezone.utcoffset(-5))
    now = nowa()
    # print('now', now)
    print(len(appts), appts)
    if len(appts) != 0:
        print(getframeinfo(currentframe()).lineno)
        for appt in appts:
            # print(repr(appt))
            # print(appt.Start.date(), datetime.today().date())
            # break
            if appt.Start.date() == datetime.today().date() and appt.Start.time() > now.time():
                print('today', appt.Start, appt.Subject)
                start_time = appt.Start.astimezone() + timedelta(hours=4)
                # start_time = start_time.replace(year=2020)
                # print(appt.Subject, 'subbed start time', start_time, 'now', now)
                how_soon = start_time - now
                # print(how_soon)

                if how_soon.total_seconds() < 1200:
                    subj = str(appt.Subject)
                    # print(subj, type(subj))
                    msg = subj + ' In {} minutes'.format(round(how_soon.seconds/60, 1))

                    get_toasty(title=subj, message=msg)
                    print(msg)
                    # qlog(msg)
                    print("{0} Start: {1}, End: {2}, Organizer: {3}".format(
                          appt.Subject, appt.Start,
                          appt.End, appt.Organizer))

    else:
        print('No appts returned.')
# check_appts_soon()