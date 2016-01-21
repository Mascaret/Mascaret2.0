# Kivy Libs imports
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty

# Python Libs imports

# Personnal Libs imports
from gui.homepagelayout.modulebutton import ModuleButton


Builder.load_string('''
############################### Home Screens ###############################

<MainScreenManager>:
    mode: "narrow" if self.width < 800 else "wide"


<HomePageScreen>:
    name: 'homepage'
    screen1_box: box
    modulebtn_box: modulebtn_box
    right_panel: right_pan
    Screen:
        name: '1'
        BoxLayout:
            id: box
            canvas.before:
                Rectangle:
                    source: 'gui/sharedpics/bg6.jpg'
                    size: root.width if (root.width / root.height) > (1920 / 1080) else root.height * (1920 / 1080), root.height if (root.width / root.height) <= (1920 / 1080) else root.width / (1920 / 1080)
                    pos: self.pos
            FloatLayout:
                GridLayout:
                    id: modulebtn_box
                    spacing: 30
                    size_hint: 0.5, 0.5
                    pos_hint: {'x': 0.25, 'y': 0.15}
                    cols: 2
            BoxLayout:
                id: right_pan

    Screen:
        name: '2'
        Button:
            # size_hint = (0.1,1)
            background_normal: ''
            background_color: (230/255, 230/255, 230/255, 0)
            text: 'Go to Screen 1'
            on_release:
                root.transition.direction = 'right'
                root.current = '1'
############################### Home Screens ###############################
''')


class HomePageScreen(Screen, ScreenManager):
# Class of the Home Page screen
    screen1_box= ObjectProperty()
    # right_Button= ObjectProperty()
    modulebtn_box= ObjectProperty()
    right_panel= ObjectProperty()

    def __init__(self, mainscreenmanager, **kwargs):
        super(HomePageScreen, self).__init__(**kwargs)
        # reference of the main screen manager
        self.mainscreenmanager = mainscreenmanager

    def add_modulebtn(self, module_id):
        self.modulebtn_box.add_widget(ModuleButton(
                                module_id = module_id,
                                mainscreenmanager = self.mainscreenmanager
                                                  )
                                     )
