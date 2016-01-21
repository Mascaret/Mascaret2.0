# Kivy libs import
from kivy.uix.colorpicker import ColorWheel
from kivy.uix.widget import Widget

# Python libs import

# Personal libs import


class AutonomousColorWheel(ColorWheel):
# This is an autonomous version of he colorwheel

    _radius = 100
    _origin = (100, 100)

    def __init__(self, color_picker_window,**kwarg):
        super(AutonomousColorWheel, self).__init__(**kwarg)
        self.color_picker_window = color_picker_window
        self.init_wheel(dt = 0)

    def on__hsv(self, instance, value):
        super(AutonomousColorWheel, self).on__hsv(instance, value)
        #Any method you want to trigger
        self.color_picker_window.color_change(self.rgba)

    # def on_radius(self, *args, **kwargs):
    #     super(AutonomousColorWheel, self).on_radius(*args, **kwargs)
    #     self._radius = min(self.width / 2, self.height / 2)
    #     self._origin = (self.width / 2, self.height / 2)
    #
    # def on_height(self, *args, **kwargs):
    #     # super(AutonomousColorWheel, self).on_height(*args, **kwargs)
    #     self._radius = min(self.width / 2, self.height / 2)
    #     self._origin = (self.width / 2, self.height / 2)
