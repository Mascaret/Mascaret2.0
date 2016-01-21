# Kivy Libs imports
from kivy.uix.button import Button

# Python libs import

#Personnal Libs imports
from gui.widget.hoverclass.hoverclass import HoverBehavior

#Buttons with a "mouse_on" effect

class HoverButton1(Button, HoverBehavior):
    mouse_on_color = (100/255, 100/255, 230/255, 1)
    mouse_out_color = (100/255, 100/255, 230/255, 0.8)

# hover effect : opacity 0.8 => 1
    def on_enter(self):
        self.background_color= self.mouse_on_color

    def on_leave(self):
        self.background_color= self.mouse_out_color


class HoverButton2(Button, HoverBehavior):
# hover effect : darker bg, no opacity change
    def on_enter(self):
        self.background_normal = 'gui/hoverclasses/rectbut2.png'

    def on_leave(self):
        self.background_normal =  'gui/hoverclasses/rectbut1.png'
