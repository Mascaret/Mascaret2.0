# Kivy libs import
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.scrollview import ScrollView
from kivy.properties import (
                            NumericProperty, ReferenceListProperty,
                            ObjectProperty
                            )
from kivy.properties import StringProperty, ListProperty, DictProperty
from kivy.event import EventDispatcher
from kivy.graphics import Color, Rectangle
from kivy.uix.colorpicker import ColorPicker

from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.splitter import Splitter
from kivy.effects.scroll import ScrollEffect
from kivy.graphics import Line
from kivy.graphics.instructions import InstructionGroup
from kivy.uix.popup import Popup

# Python libs import
import random
import calendar
import pandas as pd
from bisect import bisect_left

# Personnal Libs imports
from data.logicalobject.task import Task
from data.logicalobject.ressource import Ressource
from data.logicalobject.taskgroup import TaskGroup
from data.logicalobject.ressourcegroup import RessourceGroup
from data.db import MyDB
from gui.widget.hoverclass.hoverlabel import HoverLabel1
from ressource.function.calendartools import *
from tools.ganttool.gui.calendarscroll import CalendarHeaderScroll
from tools.ganttool.gui.gantscroll import GantMainScroll
from tools.ganttool.gui.headerscroll import HeaderScroll
from gui.widget.editwindows import (
                                    Task_Edit_Window, Ressource_Edit_Window,
                                    TaskGroup_Edit_Window, RessourceGroup_Edit_Window
                                    )

Builder.load_string('''
############################ Beginning of Gant sheet ##########################

<GantTool>:
    # UI of the Gant sheet
    # the background is defined by the canvas
    # canvas.before:
    #     Rectangle:
    #         source: 'gui/sharedpics/bg4.jpg'
    #         size: root.width if (root.width / root.height) > (1920 / 1080) else root.height * (1920 / 1080), root.height if (root.width / root.height) <= (1920 / 1080) else root.width / (1920 / 1080)
    #         pos: self.pos
        # Color:
        #     # rgba: 75/255,191/255,107/255,1
        #     rgba: 75/255,75/255,75/255,.5
        # Rectangle:
        #     size: self.size

    # This layout is displayed to have a smooth border arround the calendarscoll
    # the calendarscroll must be in front of it so we need to draw it before.
    RelativeLayout:
        # Same pos and size as the calendarscroll
        pos_hint: {'x': 0.17,'y': .94}
        size_hint: (0.81, 0.04)
        canvas.before:
            Color:
                rgba:  226/255,228/255,230/255,1
            # We draw a line around the top and the left, with round corner
            Line:
                points:
                    (self.width-6,self.height ,0,self.height,0,6)
                width: 6
                joint: 'round'
                cap: 'square'
            Rectangle:
                size: self.size

    Button:
        pos_hint: {'x': 0.08,'y': 0.94}
        # size_hint: (0.10, 0.04)
        size_hint: (None, None)
        size: (24,24)
        background_color: [0,0,0,0.5]
        # text: "add a resource"
        on_release: root.new_ressource()
        background_normal: 'gui/sharedpics/plus2.png'

    Button:
        pos_hint: {'x': 0.06,'y': 0.94}
        # size_hint: (0.10, 0.04)
        size_hint: (None, None)
        size: (24,24)
        background_color: [0,0,0,0.5]
        # text: "add a taskgroup"
        on_release: root.new_taskgroup()
        background_normal: 'gui/sharedpics/plus2.png'

    Button:
        pos_hint: {'x': 0.04,'y': 0.94}
        # size_hint: (0.10, 0.04)
        size_hint: (None, None)
        size: (24,24)
        background_color: [0,0,0,0.5]
        # text: "add a ressource group"
        on_release: root.new_ressourcegroup()
        background_normal: 'gui/sharedpics/plus2.png'

    # Button:
    #     pos_hint: {'x': 0,'y': 0}
    #     size_hint: (0.10, 0.05)
    #     text: "test"
    #     on_release: root.met1()
    # Button:
    #     pos_hint: {'x': 0.2,'y': 0}
    #     size_hint: (0.10, 0.05)
    #     text: "test2"
    #     on_release: root.met2()
    # Button:
    #     pos_hint: {'x': 0.4,'y': 0}
    #     size_hint: (0.10, 0.05)
    #     text: "test3"
    #     on_release: root.met3()
    # Button:
    #     pos_hint: {'x': 0.6,'y': 0}
    #     size_hint: (0.10, 0.05)
    #     text: "add a task"
    #     on_release: root.met4()
    # Button:
    #     pos_hint: {'x': 0.8,'y': 0}
    #     size_hint: (0.10, 0.05)
    #     text: "add a resource"
    #     on_release: root.met5()

############################## End of Gant Layout #############################

''')


class GantTool(FloatLayout):

##################### Constructeur #####################
    def __init__(self, first_day = "2015-09-01",
                        last_day = "2015-11-30", **kwargs):
        super(GantTool, self).__init__(**kwargs)

        # this var handles the way the scrolling works between the different
        # scrolls
        # the use of the "being_scrolled" var prevent from a loop between
        # the update_from_scroll method of all the scrollview to occur
        self.being_scrolled = False

        # We build the GUI
        self.build_GUI()

        # we init the height of row displayed
        self.set_row_height(50)

        # we init the list of the days displayed
        self.update_days_dataframe(
                        new_days_list = build_list_of_days(
                                                        first_day=first_day,
                                                        last_day = last_day
                                                          ),
                        new_day_width = 100,
                        init = True
                                    )
        # print(self.days_dataframe)

        #init of the db
        self.mydb = MyDB()

        # we get the task groups
        self.taskgroups_dataframe = self.mydb.get_dataframe(objct = TaskGroup)

        # we get the ressource groups
        self.ressourcegroups_dataframe = self.mydb.get_dataframe(
                                                        objct = RessourceGroup
                                                                )

        # we get the ressources
        self.ressources_dataframe = self.mydb.get_dataframe(objct = Ressource)
        print(self.ressources_dataframe )
        # and we add each ressource in the dataframe
        for ix in self.ressources_dataframe.index:
            self.add_ressource(self.ressources_dataframe.ix[ix], init = True)

        self.tasks_dataframe = self.mydb.get_dataframe(objct = Task)
        # print(self.tasks_dataframe)
        # and we add each task in the dataframe
        for ix in self.tasks_dataframe.index:
            self.add_task(self.tasks_dataframe.ix[ix], init = True)



    def update_days_dataframe(
                                self,
                                new_days_list = [],
                                new_day_width = 0,
                                init = False
                              ):
    # This method update the days_dataframe according to:
    #     a new day list if so
    #     a new day width if so
    # If the init attr is = True, it creates the objects
    # self.number_of_days and self.day_width before creating the dtf
    # Using the init without any new_day... will create an empty dtf

        # if it's an init we need to create the var
        if init == True:
            self.day_width = new_day_width
            self.number_of_days = len(new_days_list)
            self.init_days_dataframe(self.number_of_days)
            self.days_dataframe.date = new_days_list
            self.days_dataframe.absc = self.get_address_list(
                                number_of_days = self.number_of_days,
                                day_width = self.day_width
                                                            )
            self.calendar_scrollview.days_list_upd()
            self.gant_scrollview.days_list_upd()

        else:

            # If there is a new day_list then we need to update the dtf
            if new_days_list != []:
                # If there is a new day width then
                if new_day_width != 0:
                    self.day_width = new_day_width
                    # the number of days in the new days_list
                    new_number_of_days = len(days_list)
                    # If this number of days is != from the old number_of_days,
                    # we need to re-create a new dtf
                    if self.number_of_days != new_number_of_days:
                        self.number_of_days = new_number_of_days
                        self.init_days_dataframe(new_number_of_days)

                        self.days_dataframe.date = days_list
                        self.days_dataframe.absc = self.get_address_list(
                                        number_of_days = new_number_of_days,
                                        day_width = self.day_width
                                                    )

                        self.calendar_scrollview.days_list_upd()
                        self.gant_scrollview.days_list_upd()
                    # Else we dont need a new dtf, we can just replace values
                    # in the current one
                    else:
                        self.days_dataframe.date = days_list
                        self.days_dataframe.absc = self.get_address_list(
                                        number_of_days = new_number_of_days,
                                        day_width = self.day_width
                                                                    )
                        self.calendar_scrollview.days_list_upd()
                        self.gant_scrollview.days_list_upd()
                # If the day_widh is the same
                else:
                    # the number of days in the new days_list
                    new_number_of_days = len(new_days_list)
                    # If this number of days is != from the old number_of_days,
                    # we need to re-create a new dtf
                    if self.number_of_days != new_number_of_days:
                        self.number_of_days = new_number_of_days
                        self.init_days_dataframe(new_number_of_days)

                        self.days_dataframe.date = new_days_list
                        self.days_dataframe.absc = self.get_address_list(
                                        number_of_days = new_number_of_days,
                                        day_width = self.day_width
                                                                    )

                        self.calendar_scrollview.days_list_upd()
                        self.gant_scrollview.days_list_upd()
                    # if the number of day is the same AND the day width, we
                    # just need t update the dates list in the dtf
                    else:
                        self.days_dataframe.date = new_days_list

                        self.calendar_scrollview.days_list_upd()
                        self.gant_scrollview.days_list_upd()
            # If there is no new_day_list
            else:
                # If there is a new day width then we just need to update the
                # absc list in the dtf
                if new_day_width != 0:
                    self.day_width = new_day_width
                    self.days_dataframe.absc = self.get_address_list(
                                        number_of_days = self.number_of_days,
                                        day_width = self.day_width
                                                                )

                    self.calendar_scrollview.day_width_upd()
                    self.gant_scrollview.day_width_upd()

    def init_days_dataframe(self, number_of_days):
        self.days_dataframe = pd.DataFrame(index = range(number_of_days),
                    columns = ['date','absc'])



    def update_day_width_display(self):
        # We update the calendar accordingly
        self.calendar_scrollview.day_width = value
        # # We update the gant accordingly
        self.gant_scrollview.day_width = value


    def update_days_list_display(self, days_list):
        # We update the calendar accordingly
        self.calendar_scrollview.days_list_upd()
        # # We update the gant accordingly
        self.gant_scrollview.days_list_upd()



    def get_address_list(self, number_of_days, day_width):
        address_list = []
        for i in range(number_of_days):
            address_list.append(i * day_width)
        return address_list


    def set_row_height(self, value):
        # we save the width in a var
        self.row_height = value
        # # We update the calendar accordingly
        self.gant_scrollview.row_height_upd()
        # The height of the header is controled by the height of the gant


    def add_ressource(self, ressource, init = False):
        if init == False:
            # we add the ressource in the var only if we are not at the init
            # of the project
            self.ressources_dataframe.ix[ressource.name] = ressource
        # We update the header accordingly
        self.header_scrollview.add_ressource(ressource.name)
        # We update the gant accordingly
        self.gant_scrollview.add_ressource(ressource.name)


    def update_ressource(self, ressource):
        self.ressources_dataframe.ix[ressource.name] = ressource

        # We update the header accordingly
        self.header_scrollview.ressource_updated(ressource.name)
        # We update the gant accordingly
        self.gant_scrollview.ressource_updated(ressource.name)


    def add_task(self, task, init = False):
        if init == False:
            # we add the tasks in the var only if we are not at the init
            # of the project
            self.tasks_dataframe.ix[task.name] = task
        # We update the gant accordingly
        self.gant_scrollview.add_task(task.name)

    def add_taskgroup(self, taskgroup, init = False):
        if init == False:
            # we add the taskgroups in the var only if we are not at the init
            # of the project
            self.taskgroups_dataframe.ix[taskgroup.name] = taskgroup

    def add_ressourcegroup(self, ressourcegroup, init = False):
        if init == False:
            # we add the taskgroups in the var only if we are not at the init
            # of the project
            self.ressourcegroups_dataframe.ix[
                            ressourcegroup.name
                                             ] = ressourcegroup


    def delete_ressource(self, ressource_id = 1):
        self.ressources_dataframe = self.ressources_dataframe[
                            self.ressources_dataframe.index != ressource_id]
        self.header_scrollview.delete_ressource(ressource_id)
        self.gant_scrollview.delete_ressource(ressource_id)
        # need to delete the task inside!

    def delete_task(self, task_id):
        self.tasks_dataframe = self.tasks_dataframe[
                            self.tasks_dataframe.index != task_id]
        self.gant_scrollview.delete_task(task_id)

    def delete_all_ressources(self):
        self.header_scrollview.delete_all_ressources()
        self.gant_scrollview.delete_all_ressources()

    def delete_all_tasks(self):
        self.gant_scrollview.delete_all_tasks()


    def set_task_list(self):
        # self.gant_scrollview.task_list = task_list
        pass



    def met1(self):
        # This methode will be used to change the range of dates being
        # displayed
        # self.update_days_dataframe(new_days_list=
        #                     ['2015-09-01','2015-09-02','2015-09-03'])

        CP = RessourceGroup_Edit_Window(
                                title = "New RessourceGroup",
                                project = self,
                                size_hint = (None, None),
                                size = ("480dp", "400dp")
                                    )
        CP.open()


    def met2(self):
        # # This metode will be used to change the width of day columns
        # self.update_days_dataframe(new_day_width = self.day_width - 10)

        TEW = Task_Edit_Window(
                                title = "New Task",
                                project = self,
                                size_hint = (None, None),
                                size = (700, 350)
                                   )
        TEW.open()

    def new_task(self, ressource_id = 1):
        TEW = Task_Edit_Window(
                                title = "New Task",
                                project = self,
                                ressource_id = ressource_id,
                                size_hint = (None, None),
                                size = (700, 350)
                                   )
        TEW.open()

    def met3(self):

        REW = Ressource_Edit_Window(
                                title = "New Ressource",
                                project = self,
                                size_hint = (None, None),
                                size = (700, 200)
                                   )
        REW.open()



    def new_ressource(self):

        REW = Ressource_Edit_Window(
                                title = "New Ressource",
                                project = self,
                                size_hint = (None, None),
                                size = (700, 200)
                                   )
        REW.open()


    def met4(self):

        CP = TaskGroup_Edit_Window(
                                title = "New TaskGroup",
                                project = self,
                                size_hint = (None, None),
                                size = ("480dp", "400dp")
                                    )
        CP.open()

    def new_taskgroup(self):
        CP = TaskGroup_Edit_Window(
                                title = "New TaskGroup",
                                project = self,
                                size_hint = (None, None),
                                size = ("480dp", "400dp")
                                    )
        CP.open()


    def new_ressourcegroup(self):
        CP = RessourceGroup_Edit_Window(
                                title = "New RessourceGroup",
                                project = self,
                                size_hint = (None, None),
                                size = ("480dp", "400dp")
                                    )
        CP.open()

    def met5(self):
        from kivy.core.window import Window
        # Window.maximize()
        # Window.close()
        # Window.minimize()
        # Window.toggle_fullscreen()
        # if Window.borderless == True:
        #     Window.borderless = False
        # else:
        #     Window.borderless = True
        pass

    def build_GUI(self):
        # L'interface graphique du mdule
        # Elle affiche 3 principaux objets :

        # Un objet "calendar_scrollview" qui est la zone scrollable haute, dans
        # laquelle on interragit avec les dates.
        self.calendar_scrollview = CalendarHeaderScroll(
                                            project = self,
                                            pos_hint = {'x': 0.17,'y': .94},
                                            size_hint = (0.81, 0.04)
                                            )

        # Un objet "Gant_scrollview" qui est la zone scrollable centrale, dans
        # laquelle on interragit avec les tests.
        self.gant_scrollview = GantMainScroll(
                                            project = self,
                                            pos_hint = {'x': 0.17,'y': .02},
                                            size_hint = (0.81, 0.92)
                                            )

        # Un objet "header_scrollview" qui est la zone scrollable
        # gauche, dans laquelle on interragit avec les ressources.
        self.header_scrollview = HeaderScroll(
                                            project = self,
                                            pos_hint = {'x': 0.02,'y': .02},
                                            size_hint = (0.15, 0.92)
                                            )

        # we display these 3 objects
        self.add_widget(self.calendar_scrollview)
        self.add_widget(self.gant_scrollview)
        self.add_widget(self.header_scrollview)
