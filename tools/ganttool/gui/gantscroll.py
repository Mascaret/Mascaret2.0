# Kivy libs import
from kivy.lang import Builder
from kivy.uix.stacklayout import StackLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.effects.scroll import ScrollEffect
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.splitter import Splitter
from kivy.properties import NumericProperty, ObjectProperty
from kivy.properties import ListProperty
from kivy.uix.button import Button
from kivy.uix.splitter import SplitterStrip

# Python libs import
import win32api
import win32con

# Personal libs import
from gui.widget.hoverclass.hoverclass import HoverBehavior
from gui.widget.hoverclass.hoverlabel import HoverLabel1
from gui.widget.hoverclass.hoversplitterstrip import HoverSplitterStrip
from gui.widget.editwindows import Task_Edit_Window
from ressource.function.numoperation import NumOperation


Builder.load_string('''
########################### Beginning of Main Items ###########################

<MainItem>:
    size_hint: (1, None)
    # the background of one equipment planning area
    canvas:
        Color:
            rgba: 226/255,228/255,230/255,0.8
        Rectangle:
            size: self.size #(self.width + 120, self.height + 20)
        # Change the color for the drawing of the border lines
        Color:
            rgba: 226/255,228/255,230/255,0.8
        # the line at the bottom of the object
        Line:
            points:
                (self.width,-2,0,-2)
            width: 4
        # the line at the top of the object
        Line:
            points:
                (self.width,self.height+2,0,self.height+2)
            width: 4

############################## End of Main Items ##############################

########################### Beginning of Task Items ###########################

<TaskItem>:
    splitter: splitter
    task_name_label: lab
    size_hint: None, None
    size: splitter.size
    canvas:
        Color:
            rgba: (77/255,77/255,77/255,1)
        Rectangle:
            size: self.size
    MySplitter:
        id: splitter
        # strip_cls: gs.MySplitterStrip
        sizable_from: 'right'
        strip_size: '10dp'
        on_release: root.resized()
        HoverLabel1:
            id: lab
            opacity: 0.8
            canvas.before:
                Color:
                    rgba: root.task_group_color
                # Line:
                #     points: (3,self.height-2,2,self.height-2,2,2,3,2)
                #     width: 2
                #     joint: 'round'
                #     cap: 'square'
                Rectangle:
                    size: (self.width - 4, self.height)
                    pos: (4,0)
            # color: 200/255,200/255,200/255,1
            text: ""


############################## End of Task Items ##############################
''')

class GantMainScroll(ScrollView):
# Class of a scrollview displaying a gant planning
# It must be used with a calendar scrollview and a heading scrollview

    # The gant project linked to this gantmainscroll. The gant project
    # gathers the mainscrollview, the calendarscrollview and the
    # headerscrollview in one single object.
    project = ObjectProperty(None)

    # One attirbute is the width of the days
    day_width = NumericProperty()

    # One attribute is the list of days displayed
    days_list = ListProperty([])

    # The height of a row
    row_height = NumericProperty()

    # Builder:
    def __init__(self, project, **kwargs):
        super(GantMainScroll, self).__init__(**kwargs)

        # The project gathering the different scrollview in one tool
        self.project = project

        # init of the GUI
        self.build_GUI()

        # init of the dictionnary of objects
        self.ressource_items_dict = {}
        self.task_items_dict = {}


    def add_ressource(self, ressource_id):
    # this methode add the ressource item
        self.ressource_items_dict[ressource_id] = MainItem(
                                ressource_id = ressource_id,
                                project = self.project
                                )
        self.ressources_Container.add_widget(
                            self.ressource_items_dict[ressource_id])

    def add_task(self, task_id):
    # this methode add the task item
        self.task_items_dict[task_id] = TaskItem(
                                task_id = task_id,
                                project = self.project
                                                )

        self.ressource_items_dict[
            self.project.tasks_dataframe.ix[task_id].ressource_id
                                 ].add_widget(
                                            self.task_items_dict[task_id]
                                             )

        self.task_items_dict[task_id].y_positionning()

    def ressource_updated(self, ressource_id):
    # this methode upd the ressource item
        self.ressource_items_dict[ressource_id].ressource_updated()
    #
    # def update_task(self, task):
    # # this methode add the task item
    #     ix = task.name
    #     self.task_items_dict[ix].task = task

    def delete_ressource(self, ressource_id):
        # Clear the ressources with the id = ressource_id
        self.ressources_Container.clear_widgets(
                                [self.ressource_items_dict[ressource_id]])
        del self.ressource_items_dict[ressource_id]

    def delete_task(self, task_id, ressource_id):
        # Clear the tasks with the id = task_id
        self.ressource_items_dict[ressource_id].clear_widgets(
                                            [self.task_items_dict[task_id]]
                                                             )
        del self.task_items_dict[task_id]

    def delete_all_ressources(self):
        # clear all the displayed ressource items
        self.ressources_Container.clear_widgets()
        self.ressource_items_dict.clear()

    def delete_all_tasks(self):
        # clear all the displayed task items
        self.tasks_Container.clear_widgets()
        self.task_items_dict.clear()

    def days_list_upd(self):
        # When the list of days to disply change, the display is updated

        # By first clearing the current date objects
        for ressource_area in self.ressource_items_dict.values():
            ressource_area.clear_widgets()

        # Change the width of the ressources_container according to
        # the new list of days and the day width
        self.ressources_Container.width = (
                                    self.project.day_width *
                                    self.project.number_of_days
                                            )

        # And recreate the task we need
        ######################################


    def day_width_upd(self):
    # When the width of one day change

        # We update the container width
        self.ressources_Container.width = (
                                    self.project.day_width *
                                    self.project.number_of_days
                                            )

        # we update the place and size of the tasks
        ######################################
        for task_item in self.task_items_dict.values():
            # we ressize the task objects
            task_item.upd_width_from_dtf()
            # we replace it on the x axis
            task_item.upd_x_from_dtf()
            # we update the max & min width of the splitter
            task_item.upd_min_max_width()

    def row_height_upd(self):
    # When the height of rows changes
        # we ressize the ressources area
        for ressource_area in self.ressource_items_dict.values():
            ressource_area.upd_height()

        # For each task object in the gant:
        for task_item in self.task_items_dict.values():
            # we ressize the task objects
            task_item.upd_height()
            # we replace it on the y axis
            task_item.upd_y_from_dtf()


    def update_from_scroll(self, *largs):
        super(GantMainScroll, self).update_from_scroll(*largs)
        # this methode handles the scroll of this scroll and the other linked
        # scrolls
        if self.project.being_scrolled == False:
            # the use of the "being_scrolled" var prevent from a loop between
            # the update_from_scroll method of all the scrollview to occur
            # We define it at true at the beginning so update_from_scroll method
            # of the other scrollview don't trigger back
            self.project.being_scrolled = True

            # The scroll of the gant on yaxis triggers a scroll of the header
            self.project.header_scrollview.scroll_y = self.scroll_y
            self.parent.header_scrollview.update_from_scroll()

            # The scroll of the gant on xaxis triggers a scroll of the calendar
            self.parent.calendar_scrollview.scroll_x = self.scroll_x
            self.parent.calendar_scrollview.update_from_scroll()

            # enable back the scroll methods of other scrollviews
            self.project.being_scrolled = False

    def build_GUI(self):
        # We define the way the scroll works.
        self.scroll_timeout = 10
        self.effect_cls = ScrollEffect
        self.bar_width = "20dp"
        self.scroll_type = ['bars']

        # We define the "ressources_container" which is the layout inside
        # the scrollview, containing the ressource objects
        self.ressources_Container = RelativeLayout()
        # self.ressources_Container.bind(minimum_height =
        #                         self.ressources_Container.setter('height'))
        self.ressources_Container.size_hint = None, None
        # self.ressources_Container.orientation = 'lr-tb'
        # self.ressources_Container.spacing = 60
        self.add_widget(self.ressources_Container)



class MainItem(RelativeLayout):

    # Minimum amount of rows
    minimum_rows = 4

    # Constructeur
    def __init__(self, ressource_id, project, **kwargs):
        super(MainItem, self).__init__(**kwargs)
        # Init of the ressource id
        self.ressource_id = ressource_id
        # init of the project
        self.project = project
        # Init of the height of the ressource area
        self.upd_height()

    def add_row(self):
    # when a task object is higher than the highest row of the ressource area
    # minus one, we need to add a new row
        self.update_ress_attr_in_dtf(
                                    'ressource_row',
                                    self.get_ress_attr('ressource_row') + 1
                                    )
        self.upd_height()

    def delete_last_row(self):
    # when no task object is on the highest row of the ressource area
    # minus one, we need to delete a row
        # lr is the topest row of the ressource area
        lr = self.get_ress_attr('ressource_row')

        # we get the max row of this ressources' tasks
        max_row = max(
                        self.project.tasks_dataframe[
            self.project.tasks_dataframe.ressource_id == self.ressource_id
                                   ].task_row
                     ) + 1
        # if the max row of the tasks is lower than the highest row of the
        # ressource area AND Higher than the minimum row => delete
        if lr > max_row and lr >= self.minimum_rows:
            self.update_ress_attr_in_dtf('ressource_row', max_row)
            self.upd_height



    def upd_height(self):
    # This method update the height of the ressource area according to the
    # ressource dtf
        # update the ressource area
        try:
            if hasattr(self.project,'tasks_dataframe'):
                children_max_row = max(
                                self.project.tasks_dataframe[
                    self.project.tasks_dataframe.ressource_id == self.ressource_id
                                                            ].task_row
                                      ) + 2
            else:
                children_max_row = 0
        except:
            children_max_row = 0

        self.update_ress_attr_in_dtf('ressource_row',min(
                                            children_max_row,
                                            self.get_ress_attr('ressource_row')
                                                        )
                                    )

        self.height = int(
                        max(
                                self.get_ress_attr('ressource_row'),
                                self.minimum_rows
                            ) * self.project.row_height
                         )
        # We update the header
        self.project.header_scrollview.ressource_items_dict[
                                                    self.ressource_id
                                                       ].height = self.height

    def update_ress_attr_in_dtf(self, attr, value):
    # Method to change the wanted attr in the general ressource dtf
        self.project.ressources_dataframe.loc[self.ressource_id, attr] = value

    def get_ress_attr(self, attr):
    # Method to get the required attr in the ressource dtf
        return self.project.ressources_dataframe.loc[self.ressource_id, attr]

    def ressource_updated(self):
        pass

    # def on_touch_down(self, touch, *args):
    #     super(MainItem, self).on_touch_down(touch, *args)
    #     if self.collide_point(touch.x,touch.y):
    #         print('touched')
    #         print('touch.pos: ' + str(touch.pos))


class MySplitter(Splitter):

    strip_cls = ObjectProperty(HoverSplitterStrip)

    def __init__(self, **kwargs):
        super(MySplitter,self).__init__(**kwargs)
        pass


class TaskItem(ScatterLayout):

    splitter = ObjectProperty(None)

    task_name_label = ObjectProperty(None)

    task_group_color = ListProperty([77/255,77/255,77/255,1])

    def __init__(self, project, task_id, **kwargs):
        super(TaskItem, self).__init__(**kwargs)

        # init of the project
        self.project = project

        # the task the object is linked to
        self.task_id = task_id

        # Update of the min and max width of the splitter
        self.upd_min_max_width()

        # the width of the object, according to the number of days of it
        self.upd_width_from_dtf()

        # Place the object acording to it's starting day in the dtf
        self.upd_x_from_dtf()

        # Update the label on the object acording to the name of the task
        self.upd_task_name()

        # Update of the height of the object
        self.upd_height()

        # Update the y position of the object
        self.upd_y_from_dtf()

        # Update the color of the task according to it's task group
        self.upd_color()



    def upd_min_max_width(self):
        self.splitter.min_size = self.project.day_width - 1
        self.splitter.max_size = (
                                    self.project.day_width *
                                    self.project.number_of_days - 1
                                 )

    def upd_task_name(self):
    # upd the text on the object according to the name of the task
        self.task_name_label.text = self.get_task_attr('task_name')


    def upd_width_from_dtf(self):
    # the width of the object, according to the number of days of it

        self.splitter.width = (
                                int(self.get_task_attr('task_days')) *
                                int(self.project.day_width)
                                - 1
                              )


    def upd_x_from_dtf(self):
    # Place the object acording to it's starting day in the dtf
        self.x = int(
                self.project.days_dataframe[
            self.project.days_dataframe.date == self.get_task_attr('task_start')
                                           ].absc
                    )

    def upd_height(self):
    # update the height of the object
        self.splitter.height = self.project.row_height - 1

    def upd_y_from_dtf(self):
    # We update the place of the object acording to the dtf
        self.y = (
                        self.get_task_attr('task_row') *
                        self.project.row_height
                       )


    def on_transform_with_touch(self, touch):
        super(TaskItem, self).on_transform_with_touch(touch)
        # this method triggers when the task object is moved with the mouse
        mycursor = win32api.LoadCursor(0,win32con.IDC_HAND)
        win32api.SetCursor(mycursor)

        # we get the closest absc in the columns absc
        theclosest = NumOperation.takeClosest(
                                myList = self.project.days_dataframe.absc,
                                myNumber = touch.x - self.width/2
                                                )

        # the object is moved to this column absc
        self.x = theclosest[0]

        # And we save the new beginning day in the task dataframe
        self.update_task_attr_in_dtf(
                                    'task_start',
                                    self.project.days_dataframe.loc[
                                            theclosest[1],
                                            'date'
                                                                   ]
                                    )

        # we pos the object on the y absc
        self.y_positionning()

        # we update the y pos of all the other task objects according to
        for wid in self.parent.children:
            wid.y_positionning()

        # # if needed the last row of the ressource area must be deleted
        # self.parent.delete_last_row()


    def y_positionning(self):
        # to find the good pos on the y axis, we need to check that we don't
        # have any colliding issue with other task objeects

        # To do that we begin at the first row
        i = 0
        self.y = i * self.project.row_height
        # and while there is a colliding issue we step up
        while self.colliding():
            i += 1
            self.y = i * self.project.row_height

        # when finished we update the task row in the dtf
        self.update_task_attr_in_dtf('task_row', i)

        # if i + 1 == self.parent.get_ress_attr('ressource_row'):
        self.parent.update_ress_attr_in_dtf(
                'ressource_row',
                max(self.parent.get_ress_attr('ressource_row'),i + 2)
                                           )
        self.parent.upd_height()

        # # if needed the last row of the ressource area must be deleted
        # self.parent.delete_last_row()


    def resized(self):

        # we update the dtf we the new days value
        self.update_task_attr_in_dtf(
                                'task_days',
                                NumOperation.takeClosest(
                                    myList = self.project.days_dataframe.absc,
                                    myNumber = self.splitter.width
                                                         )[1]
                                    )
        # and we update the width accordinf to the dtf
        self.upd_width_from_dtf()

        # we pos the object on the y absc
        self.y_positionning()

        # we update the y pos of all the other task objects according to
        for wid in self.parent.children:
            wid.y_positionning()

        # # if needed the last row of the ressource area must be deleted
        # self.parent.delete_last_row()


    def colliding(self):
        result = False
        for wid in self.parent.children:
            if self.task_id != wid.task_id and self.collide_widget(wid):
                result = True
                break
        return result


    def update_task_attr_in_dtf(self, attr, value):
    # this method update the task attr in the dtf aocording t the value
        self.project.tasks_dataframe.loc[self.task_id, attr] = value


    def get_task_attr(self, attr):
    # this method get the task attr in the dtf
        return self.project.tasks_dataframe.loc[self.task_id, attr]


    def upd_color(self):
        taskgroup_id = self.get_task_attr('task_group_id')
        self.task_group_color = [
            self.project.taskgroups_dataframe.loc[taskgroup_id, 'taskgroup_r'],
            self.project.taskgroups_dataframe.loc[taskgroup_id, 'taskgroup_g'],
            self.project.taskgroups_dataframe.loc[taskgroup_id, 'taskgroup_b'],
            1
                                ]

        if (
            self.task_group_color[0] +
            self.task_group_color[1] +
            self.task_group_color[2]
           ) > 1.5:
            self.task_name_label.color = [0,0,0,1]
        else:
            self.task_name_label.color = [1,1,1,1]

    def on_touch_down(self, touch, *args):
        super(TaskItem,self).on_touch_down(touch,*args)
    # This method triggers when the task object is touched by a click
        # If the mouse cursor is on the task object when the click occurs then
        if self.collide_point(touch.x,touch.y):
            # If it's a double click
            if touch.is_double_tap:
                # we create a 'task edit window'
                TEW = Task_Edit_Window(
                                    title = self.get_task_attr('task_name'),
                                    project = self.project,
                                    task_id = self.task_id,
                                    size_hint = (None, None),
                                    size = (700, 400)
                                      )
                # and display it
                TEW.open()
