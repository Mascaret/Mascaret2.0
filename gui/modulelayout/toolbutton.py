# Kivy Libs imports

# Python Libs imports

# Personnal Libs imports
from gui.widget.hoverclass.hoverbutton import HoverButton1


class ToolButton(HoverButton1):
# Class of the tool button inside the module layout

    def __init__(self, tool_id, modulescreenmanager, mainscreenmanager, **kwargs):
        super(ToolButton, self).__init__(**kwargs)
        # we get the id of the tool launched by this btn
        self.tool_id = tool_id
        # we get the screen manager containing the layout containing this btn
        self.modulescreenmanager = modulescreenmanager

        self.mainscreenmanager = mainscreenmanager

        self.build_GUI()

    def build_GUI(self):
        # we get the name of the tool, to display it on the button
        self.text = self.get_tool_attr(attr = 'tool_name')
        # init of the bg
        self.background_normal = 'gui/hoverclasses/rectbut1.png'
        self.background_color = self.mouse_out_color

    def get_tool_attr(self, attr):
    # Method to get the required attr in the tool dtf
        return self.mainscreenmanager.tools_dataframe.loc[self.tool_id, attr]

    def on_release(self):
    # the module layout displays the toolk
        self.modulescreenmanager.show_tool(tool_id = self.tool_id)
