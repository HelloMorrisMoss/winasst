# from tkinter import *
# from tkinter.messagebox import showinfo
#
# def reply(name, event=None):
#     src = event.widget
#     text = src.get()
#     showinfo(title="Reply", message = "Hello %s!" % text)
#     # print(event)
#
#
# top = Tk()
# top.title("Echo")
# # top.iconbitmap("Iconshock-Folder-Gallery.ico")
#
# Label(top, text="Enter your name:").pack(side=TOP)
# ent = Entry(top)
# ent.bind("<Return>", (lambda event: reply(ent.get(), event)))
# ent.pack(side=TOP)
# btn = Button(top,text="Submit", command=(lambda event: reply(ent.get(), event)))
# btn.pack(side=LEFT)
#
# top.mainloop()


import tkinter as tk
import sqlite3

root = tk.Tk()
# canv1 = tk.Canvas(root, width=400, height=300)
# in_box = tk.Entry(root)
# canv1.create_window(200, 140, window=in_box)

# def

# input_text = tk.StringVar()


# TODO's:
#  enter also performs action
#  still last thing button
#  other recent things buttons
#  send the data somewhere (looking at the sqlite import up there)
#  pop up when stretch reminder?
#  timeout
#  detect afk?

label1 = tk.Label(root, text='''What's up?''')
label1.grid(row=0, column=0)
# label1.pack()


def text_entered(widget):
    # print('running test fn print_text')
    # print(form1.get())
    label1.config(text=widget.get())

form1 = tk.Entry(root)
form1.grid(row=1, column=0)
form1.bind("<Return>", (lambda event: text_entered(event.widget)))

b1 = tk.Button(root, text="enter", command=lambda: text_entered(form1))
# b1.pack()
b1.grid(row=2, column=0)

for i in range(1, 3):
    btn = tk.Button(root, text=f'button {i}')
    btn.grid(row=2+i, column=0)


# in_box = tk.Entry(root)
# in_box.pack()

root.mainloop()