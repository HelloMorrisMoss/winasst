"""Trying to open/control VLC player
vlc-ctrl is linux only

https://pypi.org/project/python-vlc/ pure python
https://wiki.videolan.org/Python_bindings/
https://www.olivieraubert.net/vlc/python-ctypes/doc/

despite many options claiming to control volume, none actually work
https://wiki.videolan.org/Documentation:Command_line/


using socket to control
https://stackoverflow.com/a/61485122/10941169
"""

# from https://stackoverflow.com/a/62509310/10941169
from vlc import Instance
import time
import os
from traceback import format_exc as exc


class VLC:
    def __init__(self):
        self.Player = Instance('--loop')

    def addPlaylist(self):
        self.mediaList = self.Player.media_list_new()
        # path = r"C:\Users\lmcglaughlin\Music"
        path = r"C:\Users\lmcglaughlin\Google Drive\Study"
        songs = os.listdir(path)
        for s in songs:
            self.mediaList.add_media(self.Player.media_new(os.path.join(path,s)))
        self.listPlayer = self.Player.media_list_player_new()
        self.listPlayer.set_media_list(self.mediaList)
    def play(self):
        self.listPlayer.play()
    def next(self):
        self.listPlayer.next()
    def pause(self):
        self.listPlayer.pause()
    def previous(self):
        self.listPlayer.previous()
    def stop(self):
        self.listPlayer.stop()
    def show(self):
        # doesn't exist
        self.listPlayer.show()
    def close(self):
        self.listPlayer.release()
    # def vol_up(self):
    #     self.listPl

try:
    vinstance = VLC()
    vinstance.addPlaylist()
    # vinstance.show()
    vinstance.next()
    vinstance.play()
    time.sleep(5)
except:
    print(exc())
finally:
    vinstance.close()