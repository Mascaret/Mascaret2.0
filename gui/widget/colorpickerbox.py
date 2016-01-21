# Kivy libs import
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button

# Python libs import

# Personal libs import
from gui.widget.colorwheel import AutonomousColorWheel
from gui.widget.coloredtextinput import ColoredTextInput

class ColorPickerBox(RelativeLayout):
    def __init__(self, popupwindow, **kwargs):
        super(ColorPickerBox, self).__init__(**kwargs)

        self.popupwindow = popupwindow

        self.generator = RelativeLayout(
                                    size_hint = (None, None),
                                    width = "400dp",
                                    height = "200dp",
                                    pos = ["50dp", "100dp"]   #"50dp"
                                       )

        self.acw = AutonomousColorWheel(self)
        self.generator.add_widget(self.acw)

        self.gpi = ColoredTextInput(pos = ["230dp", "80dp"])
        self.generator.add_widget(self.gpi)

        self.add_widget(self.generator)


        self.create_btn = Button(
                                    size_hint = [None, None],
                                    size = ["100dp","30dp"],
                                    pos = ["320dp","10dp"]
                                )
        self.create_btn.bind(on_release=self.create_group)


        self.cancel_btn = Button(
                                    size_hint = [None, None],
                                    size = ["100dp","30dp"],
                                    pos = ["200dp","10dp"]
                                )
        self.cancel_btn.bind(on_release=self.cancel_creation)



        self.add_widget(self.cancel_btn)
        self.add_widget(self.create_btn)

    def create_group(self, instance):
        print("creation")
        self.popupwindow.change_group()
        self.popupwindow.dismiss()

    def cancel_creation(self, instance):
        print("cancel creation")
        self.popupwindow.dismiss()

    def color_change(self, rgba):
        self.gpi.back_color = rgba
