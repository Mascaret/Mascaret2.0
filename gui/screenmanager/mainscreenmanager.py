# Kivy Libs imports
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.properties import StringProperty

#Python Libs imports

#Personnal Libs imports
import config.settings as setts                 # Get the local default config
from data.logicalobject.user import User        # Get the user
from gui.modulelayout.modulescreen import ModuleScreen
from gui.homepagelayout.homescreen import HomePageScreen
from data.db import MyDB                        # Get the database
from data.logicalobject.users import Userd
from data.logicalobject.modules import Module
from data.logicalobject.tools import Tool
from data.logicalobject.userstools import UserTool


class MainScreenManager(ScreenManager):
# Class of the Main screenmanager

    def __init__(self, mainroot,**kwargs):
        super(MainScreenManager, self).__init__(**kwargs)
        # init of the window of the prg
        self.mainroot = mainroot
        # building of the GUI
        self.build_GUI()
        # Init the dataframes
        self.init_dataframes()
        # get and add the modules
        self.init_modules()

    def build_GUI(self):
    # GUI builder method
        # no visual transition between the different screens of the
        # main screen manager
        self.transition = NoTransition()
        # reference and add the home page
        self.homepage = HomePageScreen(mainscreenmanager = self)
        self.add_widget(self.homepage)

        # # reference and add the right panel
        # self.right_panel= RightPanel()
        # self.current_screen.screen1_box.add_widget(self.right_panel)

    def add_module(self, module_id):
        # At first we create the module screenmanager, displayed as the
        # module main page
        self.modules_dict[module_id] = ModuleScreen(
                                            name = str(module_id),
                                            module_id = module_id,
                                            mainscreenmanager = self
                                                   )
        self.add_widget(self.modules_dict[module_id])

        # then we add the module btn in the homepage
        self.homepage.add_modulebtn(module_id)


    def show_module(self, module_id):
        self.current = str(module_id)


    def init_dataframes(self):
######################### Beginning of the CSV Method #########################
        # init of the dtb
        # DB CONNECTION
        db = MyDB()

        # we get the id of the logged user
        user_id_logged = User().index

        # we get the modules dtf
        modules_dataframe = db.get_dataframe(objct = Module)

        # we get the tools dtf
        tools_dataframe = db.get_dataframe(objct = Tool)

        # we get the userstools dtf
        userstools_dataframe = db.get_dataframe(objct = UserTool)

        # we get the id of the tools available for the user
        tools_id_available = userstools_dataframe[
                            userstools_dataframe.index == user_id_logged
                                                 ].tool_index

        # we get the tools available
        self.tools_dataframe = tools_dataframe[
                            tools_dataframe.index.isin(tools_id_available)
                                              ]

        # we get the modules for the tools
        self.modules_dataframe = modules_dataframe[
                modules_dataframe.index.isin(self.tools_dataframe.module_index)
                                                  ]
############################ End of the CSV Method ############################

    def init_modules(self):

        # init of the dict of modules
        self.modules_dict = {}

        # for each module in the dtf, we add it
        for id in self.modules_dataframe.index:
            self.add_module(module_id = id)
