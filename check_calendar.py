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
from qlog import lg


def nowa():
    """Get a local timezone aware datetime for now."""
    # painful to work with dates
    # https://stackoverflow.com/a/25887393/10941169
    utc_dt = datetime.now(timezone.utc)  # UTC time
    dt = utc_dt.astimezone()
    return dt


def get_toasty(title: str, message: str, action: Callable = None):
    """Display a windows toaster notification, optionally with an action on click."""
    toaster = ts.ToastNotifier()
    clicked = toaster.show_toast(title,
                                 message,
                                 callback_on_click=action)
    if clicked:
        lg.debug('toaster notification was clicked.')


def get_appts():
    """Get appointments from outlook calendar."""
    # https://stackoverflow.com/questions/21477599/read-outlook-events-via-python
    lg.debug(getframeinfo(currentframe()).lineno)
    Outlook = win32com.client.Dispatch("Outlook.Application")

    try:
        lg.debug(getframeinfo(currentframe()).lineno)
        ns = Outlook.GetNamespace("MAPI")

        appointments = ns.GetDefaultFolder(9).Items
    except AttributeError:
        lg.debug(exc())
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
    # lg.debug('begin {} end {}'.format(begin, end))
    # # restriction = "[Start] >= '" + begin.strftime("%m/%d/%Y") + "' AND [End] <= '" + end.strftime("%m/%d/%Y") + "'"
    # # restriction1 = "[Start] >= '" + begin.strftime("%m/%d/%Y 12:00 AM") + "'"
    # # restriction2 = "'[Start] <= '" + end.strftime("%m/%d/%Y 00:00 AM") + "'"
    # # lg.debug('restriction1', restriction1)
    # # lg.debug('restriction2', restriction2)
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


def check_appts_soon():
    # tz = timezone.tz
    lg.debug('checking for appts soon.')

    # timezone
    appts = get_appts()
    # now = datetime.now().astimezone(timezone.utcoffset(-5))
    now = nowa()
    lg.debug('now ' + str(now))
    if len(appts) != 0:
        lg.debug(getframeinfo(currentframe()).lineno)
        for appt in appts:
            # lg.debug(repr(appt))
            # lg.debug(appt.Start.date(), datetime.today().date())
            # break
            if appt.Start.date() == datetime.today().date() and appt.Start.time() > now.time():
                lg.debug('today', appt.Start, appt.Subject)
                start_time = appt.Start.astimezone() + timedelta(hours=4)
                # start_time = start_time.replace(year=2020)
                # lg.debug(appt.Subject, 'subbed start time', start_time, 'now', now)
                how_soon = start_time - now
                # lg.debug(how_soon)

                if how_soon.total_seconds() < 1200:
                    subj = str(appt.Subject)
                    # lg.debug(subj, type(subj))
                    msg = subj + ' In {} minutes'.format(round(how_soon.seconds/60, 1))

                    get_toasty(title=subj, message=msg)
                    lg.debug(msg)
                    # qlog(msg)
                    lg.debug("{0} Start: {1}, End: {2}, Organizer: {3}".format(
                          appt.Subject, appt.Start,
                          appt.End, appt.Organizer))

    else:
        lg.debug('No appts returned.')

# test
if __name__ == '__main__':
    check_appts_soon()