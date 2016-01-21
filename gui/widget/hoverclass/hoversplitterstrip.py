# Kivy libs import
from kivy.uix.label import Label
from kivy.uix.splitter import SplitterStrip
from kivy.uix.button import Button
from kivy.core.window import Window

#Python Libs imports

#Personnal Libs imports
from gui.widget.hoverclass.hoverclass import HoverBehavior

#Button with a "mouse_on" effect
class HoverSplitterStrip(Button, HoverBehavior):    #, HoverBehavior

    def __init__(self, **kwargs):
        self.background_normal = "gui/login_screen/loading.jpg"
        self.background_down = "gui/login_screen/loading.jpg"
        super(HoverSplitterStrip, self).__init__(**kwargs)

        print('hvss created')


    def on_enter(self):
        print('enter')

    def on_leave(self):
        print('out')
    # mycursor = win32api.LoadCursor(0,win32con.IDC_SIZEWE)
    # pass
