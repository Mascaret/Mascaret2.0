# Kivy libs import
from kivy.uix.label import Label

#Python Libs imports

#Personnal Libs imports
from gui.widget.hoverclass.hoverclass import HoverBehavior


#Button with a "mouse_on" effect
class HoverLabel1(Label, HoverBehavior):
    def on_enter(self):
        self.opacity= 1

    def on_leave(self):
        self.opacity= 0.8
