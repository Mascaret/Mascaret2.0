# Kivy Libs imports

# Python Libs imports

# Personnal Libs imports
from gui.widget.hoverclass.hoverbutton import HoverButton1


class ModuleButton(HoverButton1):
# Class of the module button inside the home page layout

    def __init__(self, module_id, mainscreenmanager, **kwargs):
        super(ModuleButton, self).__init__(**kwargs)
        # we get the id of the module displayed by this btn press
        self.module_id = module_id
        # we get the screen manager containing the layout containing this btn
        self.mainscreenmanager = mainscreenmanager

        self.build_GUI()

    def build_GUI(self):
        # we get the name of the tool, to display it on the button
        self.text = self.get_module_attr(attr = 'module_name')
        # init of the bg
        self.background_normal = 'gui/hoverclasses/rectbut1.png'
        self.background_color = self.mouse_out_color

    def get_module_attr(self, attr):
    # Method to get the required attr in the tool dtf
        return self.mainscreenmanager.modules_dataframe.loc[self.module_id, attr]

    def on_release(self):
    # the main screen manager switches to the module
        self.mainscreenmanager.show_module(module_id = self.module_id)
