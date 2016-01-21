# Kivy Libs imports
from kivy.config import Config
Config.set('graphics', 'window_state', 'maximized')
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button

# # Python Libs imports
# import pymysql
import win32api

# Personnal Libs imports
from gui.loginlayout.mainloginlayout import MainLoginLayout
from gui.screenmanager.mainscreenmanager import MainScreenManager
from data.db import MyDB
from config.cursor import Cursor


class MascaretRoot(FloatLayout):
    # Root

    def __init__(self):
        super(MascaretRoot, self).__init__()
        # At the init of the program window, we first display the login layout
        self.show_mainloginlayout()

        self.mycursor = Cursor()

        Window.bind(mouse_pos=self.on_mouse_pos)


    def show_mainloginlayout(self):
    # Method displaying the login layout
        self.clear_widgets()
        self.add_widget(MainLoginLayout(mainroot = self))

    def after_loginscreen(self, value = 1):
    # Method triggered by the login screen
        # by default the trigger of this method build the mascaret main display
        if value == 1:
            self.show_mainscreenmanager()

    def show_mainscreenmanager(self):
    # Method displaying the mainscreenmanager, which will contain the different
    # screen of the prg (home page, setting page, module pages...)
        self.clear_widgets()
        # we build a reference to the MainScreenManager
        self.mainscreenmanager = MainScreenManager(mainroot = self)
        self.add_widget(self.mainscreenmanager)

    def on_mouse_pos(self, *args):
        # we handle here the changes of cursor
        win32api.SetCursor(self.mycursor.cursor)

#Panel containing tools on the right of the screen
class RightPanel(FloatLayout):
    pass

#button linking to the right panel
class RightPanelBtn(Button):
    pass

#App
class Mascaret(App):
    pass

Mascaret().run()
