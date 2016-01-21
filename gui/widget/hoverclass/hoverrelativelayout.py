# Kivy libs import
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Color, Rectangle, BorderImage

#Python Libs imports

#Personnal Libs imports
from gui.widget.hoverclass.hoverclass import HoverBehavior

#Button with a "mouse_on" effect
class HoverRelativeLayout1(RelativeLayout, HoverBehavior):
    def on_enter(self):
        self.opacity = 0
    def on_leave(self):
        with self.canvas:
            self.opacity = 1
            # Rectangle(source = 'gui/hoverclasses/rectbut1.png')
