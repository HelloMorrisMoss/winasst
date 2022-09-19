import tkinter as tk
import time
import threading
from managed_programs.data_dicts import procs_2_watch
from qlog import lg
from sound_i0.voice import read_this


class SettingsWindow(tk.Tk):
    def __init__(self, bg_process, settings_dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.settings_dict = settings_dict
        self.title('WinAsst GUI')
        self.geometry('400x200')

        settings_frame = tk.Frame(self)
        settings_frame.pack()

        self.chkbx_dict = {}

        for proc, params in procs_2_watch.items():
            # def add_checkbox()
            print(proc)
            cb_text = proc
            # chkbx_dict[proc] = tk.Checkbutton(settings_frame, text=cb_text).grid(sticky=tk.W)
            self.chkbx_dict[proc] = {'selected': tk.BooleanVar(), 'value': False}
            self.chkbx_dict[proc]['check_box'] = tk.Checkbutton(settings_frame, text=cb_text,
                                                                variable=self.chkbx_dict[proc]['selected']).grid(
                sticky=tk.W)
            self.chkbx_dict[proc]['selected'].set(True)

        # start the background thread
        threading.Thread(target=bg_process, args=[settings_dict], kwargs=kwargs).start()
        self.update_settings()

        self.current_task = CurrentTaskFrame(self).pack()

        def on_closing():
            # TODO: this needs to end the other thread; it may need to be wrapped in a custom stoppable thread class
            print('Window closed, ending mainloop.')
            # print('self.bg_proc', type(self.bg_proc), self.bg_proc)
            self.destroy()

        self.protocol("WM_DELETE_WINDOW", on_closing)

        self.mainloop()

    def update_settings(self):
        for k, v in self.chkbx_dict.items():
            self.settings_dict[k] = v['selected'].get()
            # print(k, v)

        self.after(1000, self.update_settings)


class CurrentTaskFrame(tk.LabelFrame):
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        super().__init__(parent, text='current task', *args, **kwargs)
        self.current_task_var = tk.StringVar()
        self.current_task_entry = tk.Entry(self, textvariable=self.current_task_var)
        self.current_task_entry.pack()
        self.current_task_minutes_var = tk.StringVar()
        self.current_task_minutes_var.set("0")
        self.current_task_seconds_var = tk.StringVar()
        self.current_task_seconds_var.set("0")
        spinbox_values = tuple(range(0, 61))
        tk.Spinbox(self, textvariable=self.current_task_minutes_var, values=spinbox_values).pack()
        tk.Spinbox(self, textvariable=self.current_task_seconds_var, values=spinbox_values).pack()
        self.running_task = tk.StringVar()
        self.running_val = 'running_val'
        self.not_running_val = 'no task'
        self.running = False
        self.start_button = tk.Checkbutton(self, onvalue=self.running_val, offvalue=self.not_running_val,
                                           textvar=self.running_task, command=self.toggle_task_running)
        self.start_button.pack()

    def toggle_task_running(self, event=None):
        if self.running:
            self.running = False
        else:
            self.running = True

    @property
    def running(self):
        return self.running_task.get() == self.running_val

    @running.setter
    def running(self, new_bool:bool):
        if new_bool:
            self.running_task.set(self.running_val)
            self.task_timer()
        else:
            self.running_task.set(self.not_running_val)

    def task_timer(self, event=None):
        if self.running:
            time.sleep(1)
            secs_int = int(self.current_task_seconds_var.get()) - 1
            self.current_task_seconds_var.set(int(secs_int))
            lg.debug(f'running timer {secs_int=}')
            if secs_int == 0:
                mins_int = int(self.current_task_minutes_var.get()) - 1
                self.current_task_minutes_var.set(str(mins_int))
                self.current_task_seconds_var.set(60)

                if mins_int % 5 == 0:
                    print('reading 5 minute warning')
                    read_this(f'{mins_int} minutes left for {self.current_task_var.get()}')
            self.parent.after(1000, self.task_timer)


if __name__ == '__main__':
    settings_d = {key: False for key in procs_2_watch.keys()}


    def wattchit(*args, **kwargs):
        print(f'wattchit (testing bg_process) was given these arguments {args=}, {kwargs=}')
        while True:
            time.sleep(30)
            print('watchit loop')
            print(settings_d)


    sw = SettingsWindow(wattchit, settings_d)
