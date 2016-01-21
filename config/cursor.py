# Kivy libs import

# Python libs import
import win32api
import win32con
# import pywintypes

# Personnal Libs imports
# import config.settings as setts
from ressource.object.singleton import Singleton

class Cursor(metaclass=Singleton): #

    def __init__(self):

        self.cursor = win32api.LoadCursor(0,win32con.IDC_ARROW)
        # self.cursor = win32api.LoadCursor(0,win32con.IDC_SIZEALL)

        self.block_flag = False

    def update(self, display = ''):

        if self.block_flag:
            return

        if display == 'grab':
            self.cursor = win32api.LoadCursor(0,win32con.IDC_SIZEALL)
        elif display == 'hand':
            self.cursor = win32api.LoadCursor(0,win32con.IDC_HAND)
        elif display == 'LRarrow':
            self.cursor = win32api.LoadCursor(0,win32con.IDC_SIZEWE)
        else:
            self.cursor = win32api.LoadCursor(0,win32con.IDC_ARROW)

    def block(self):
        self.block_flag = True

    def unblock(self):
        self.block_flag = False
