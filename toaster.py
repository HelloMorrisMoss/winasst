import win10toast as ts  # this has had it's __init__.py file replaced with the one from
# https://github.com/Charnelx/Windows-10-Toast-Notifications to enable clickable toasts
from typing import Callable


def get_toasty(title: str, message: str, action: Callable = None, *action_args):
    """Create a windows 10 toast notification.

    :param title: str
        toast popup title
    :param message: str
        toast popup body text
    :param action:
        optional Callable, such as a function, when the toast is clicked
    :rtype: None
    """

    # instantiate the toast notifier
    toaster = ts.ToastNotifier()

    # show toast with return command if supplied
    toaster.show_toast(title, message, callback_on_click=lambda: action(*action_args) if action is not None else None)


if __name__ == '__main__':
    def been_clicked(*args):
        print(args[1], args[0])

    # with a on-click function
    get_toasty("Toast notification Test", "we're testing the toast notifications!", been_clicked, 'argument 0', 'arg 1')

    # without an on-click function
    get_toasty("Toast notification Test", "we're testing the toast notifications again!")

    # the return does nothing
    get_toasty("Toast notification Test", "we're testing the toast notifications again again!", lambda:  'words')
