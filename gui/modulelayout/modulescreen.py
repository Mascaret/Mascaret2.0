# Kivy Libs imports
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.animation import Animation
from kivy.uix.togglebutton import ToggleButton

#Python Libs imports

#Personnal Libs imports
from gui.widget.hoverclass.hoverclass import HoverBehavior
from gui.modulelayout.toolbutton import ToolButton
from tools.tools import load_tool_from_id
from config.cursor import Cursor

Builder.load_string('''
########################## Beginning Module Screens ###########################

<ModuleScreen>:
    toolbtn_box: toolbtn_box
    screen1_box: box
    right_panel: right_pan
    left_panel: left_pan
    # max_button: max_button
    Screen:
        name: '1'
        RelativeLayout:
            id: box
            canvas.before:
                Rectangle:
                    source: 'gui/sharedpics/' + root.bg_wp
                    size: root.width if (root.width / root.height) > (1920 / 1080) else root.height * (1920 / 1080), root.height if (root.width / root.height) <= (1920 / 1080) else root.width / (1920 / 1080)
                    pos: self.pos
            FloatLayout:
                id: left_pan
                size_hint: (0.5,1)
                pos_hint: {'x': 0, 'y': 0}
                GridLayout:
                    id: toolbtn_box
                    spacing: 30
                    size_hint: 0.5, 0.5
                    pos_hint: {'x': 0.25, 'y': 0.15}
                    cols: 2
                Button:
                    size_hint: 0.1,0.1
                    pos_hint: {'y': 0.9}
                    text: 'HP'
                    on_release: root.manager.current = 'homepage'

            BoxLayout:
                id: right_pan
                size_hint: (None,None)
                width: box.width /2
                height: box.height
                pos: (self.width, 0)



    Screen:
        name: '2'
        Button:
            background_normal: ''
            background_color: (230/255, 230/255, 230/255, 1)
            text: 'Go to Screen 1'
            on_release:
                root.transition.direction = 'right'
                root.current = '1'

############################# End Module Screens ##############################

''')


class MaxButton(HoverBehavior, ToggleButton):
    # pass
    def on_enter(self):
        Cursor().update('hand')
        self.background_color = [0,0,0,0.8]

    def on_leave(self):
        Cursor().update()
        self.background_color = [0,0,0,0.2]


class ModuleScreen(Screen, ScreenManager):
# Class of the module screen

    toolbtn_box = ObjectProperty()
    screen1_box = ObjectProperty()
    right_panel= ObjectProperty()
    left_panel = ObjectProperty()
    # max_button = ObjectProperty()

    bg_wp = StringProperty('bg6')

    def __init__(self, module_id, mainscreenmanager, **kwargs):
        super(ModuleScreen, self).__init__(**kwargs)
        # reference of the main screen manager
        self.mainscreenmanager = mainscreenmanager
        # init of its module_id
        self.module_id = module_id
        # init of the tool buttons according to the tool_dataframe
        self.init_tools()
        # init of the gui
        self.build_GUI()

    def add_toolbtn(self, tool_id):
        # we create the button
        self.toolbtns_dict[tool_id] = ToolButton(
                                tool_id = tool_id,
                                modulescreenmanager = self,
                                mainscreenmanager = self.mainscreenmanager
                                             )
        # and we add it
        self.toolbtn_box.add_widget(self.toolbtns_dict[tool_id])


    def init_tools(self):
        # init of the dict referencing the tools buttons in the module
        self.toolbtns_dict = {}
        # init of the dict referencing the tools in the module
        self.tools_dict = {}

        # get all the tools in the tools_dataframe
        for id in self.mainscreenmanager.tools_dataframe.index:
            if self.mainscreenmanager.tools_dataframe.loc[
                                                        id,
                                                        'module_index'
                                                         ] == self.module_id:
                # and add them
                self.add_toolbtn(id)

    def get_module_attr(self, attr):
    # Method to get the required attr in the tool dtf
        return self.mainscreenmanager.modules_dataframe.loc[
                                                            self.module_id,
                                                            attr
                                                           ]

    def show_tool(self, tool_id):
        self.right_panel.clear_widgets()
        self.right_panel.add_widget(self.max_button)
        self.right_panel.add_widget(self.get_tool(tool_id))

    def maximize_tool(self):
        self.screen1_box.clear_widgets([self.left_panel])
        self.right_panel.size_hint = (1,1)
        animation = Animation(
                            x = 0,
                            duration = 0.5
                             )
        animation.start(self.right_panel)
        # print(str(-self.right_panel.x))

    def minimize_tool(self):

        animation = Animation(
                            x = self.width / 2,
                            # size = (500 , 500),
                            duration = 0.5
                             )

        # animation =  Animation(
        #                     width = 600,
        #                     duration = 5
        #                               )

        animation.bind(on_complete = self.minimize_tool_afteranim)
        animation.start(self.right_panel)


    def minimize_tool_afteranim(self, *args):
        self.right_panel.size_hint = (0.5,1)
        self.screen1_box.add_widget(self.left_panel)

    def toggle_tool_size(self, instance):
        if self.max_button.state == 'down':
            self.maximize_tool()
            return
        self.minimize_tool()

    def get_tool(self, tool_id):
    # Method getting the tool based on the tool_id
        # if the tools has already been built
        if tool_id in self.tools_dict.keys():
            return self.tools_dict[tool_id]

        self.tools_dict[tool_id] = load_tool_from_id(tool_id = tool_id)
        return self.tools_dict[tool_id]

    def build_GUI(self):
    # init of the gui
        self.bg_wp = self.get_module_attr('module_wp')
        # creation of the button handling the size of the open tool
        self.max_button = MaxButton(
            size_hint = (None,None),
            size = (64,64),
            pos_hint = {'x': 0, 'y': 0.45},
            background_color = [0,0,0,0.2],
            background_normal = 'gui/modulelayout/toggleleft.png',
            background_down = 'gui/modulelayout/toggleright.png',
            on_release = self.toggle_tool_size
                                    )

    def max_animation(self):
        pass
