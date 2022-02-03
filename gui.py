import tkinter as tk
import time
import threading
from managed_programs.data_dicts import procs_2_watch


class SettingsWindow:
    def __init__(self, bg_process, settings_dict, **kwargs):
        self.root = tk.Tk()
        self.settings_dict = settings_dict
        self.root.title('WinAsst GUI')
        self.root.geometry('400x200')

        settings_frame = tk.Frame(self.root)
        settings_frame.pack()
        # frame

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

        threading.Thread(target=bg_process, args=[settings_dict], kwargs=kwargs).start()
        self.update_settings()

        def on_closing():
            # TODO: this needs to end the other thread; it may need to be wrapped in a custom stoppable thread class
            print('Window closed, ending mainloop.')
            print('self.bg_proc', type(self.bg_proc), self.bg_proc)
            self.root.destroy()


        self.root.protocol("WM_DELETE_WINDOW", on_closing)

        self.root.mainloop()

    def update_settings(self):
        for k, v in self.chkbx_dict.items():
            self.settings_dict[k] = v['selected'].get()
            # print(k, v)

        self.root.after(1000, self.update_settings)
        


if __name__ == '__main__':
    settings_d = {key: False for key in procs_2_watch.keys()}
    #
    # def test_loop():
    #     for key, setting in settings_d.items():
    #         if
    #     print()

    def wattchit():
        while True:
            time.sleep(5)
            print('watchit loop')
            print(settings_d)

    sw = SettingsWindow(wattchit, settings_d)

