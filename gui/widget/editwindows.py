# Kivy libs import
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.properties import (
                            ObjectProperty, DictProperty,
                            StringProperty, ListProperty
                            )
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle
from kivy.uix.button import Button

# Python libs import
import pandas as pd

# Personal libs import
from gui.widget.colorpickerbox import ColorPickerBox
from gui.widget.centeredtextinput import CenteredTextInput
from gui.widget.dtbobjctdropdown import DtbObjctDropDown

Builder.load_string('''
######################## Beginning of Task Edit Window ########################

<Task_Edit_Window>:
    start_day_input: start_day_input
    name_input: name_input
    duration_input: duration_input
    comment_input: comment_input
    box_containing_taskgroup: box
    # taskgroupbtn: taskgroupbtn
    # color_box: color_input
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            StackLayout:
                size_hint: 2, 1
                padding: "10dp"
                orientation: 'tb-rl'
                BoxLayout:
                    size_hint: 1, None
                    height: "30dp"

                    Label:
                        size_hint: None, 1
                        width: "50dp"
                        text: "Test: "
                        text_size: self.size
                        valign: 'middle'
                        italic: True
                    TextInput:
                        id: name_input
                        text: "" if root.task_dict == {} else str(root.task_dict['task_name'])
                BoxLayout:
                    id: box
                    size_hint: 1, None
                    height: "30dp"

                    Label:
                        size_hint: None, 1
                        width: "100dp"
                        text: "Task group: "
                        text_size: self.size
                        valign: 'middle'
                        italic: True

            StackLayout:
                size_hint: 1.3, 1
                padding: "10dp"
                orientation: 'tb-rl'
                BoxLayout:
                    size_hint: 1, None
                    height: "30dp"
                    Label:
                        text: "Start Day: "
                        size_hint: None, 1
                        width: "150dp"
                        text_size: self.size
                        valign: 'middle'
                        italic: True
                    TextInput:
                        id: start_day_input
                        text: "" if root.task_dict == {} else str(root.task_dict['task_start'])

                BoxLayout:
                    size_hint: 1, None
                    height: "30dp"
                    Label:
                        text: "Duration (days): "
                        size_hint: None, 1
                        width: "150dp"
                        text_size: self.size
                        valign: 'middle'
                        italic: True
                    TextInput:
                        id: duration_input
                        text: "" if root.task_dict == {} else str(root.task_dict['task_days'])
        BoxLayout:
            size_hint: 1,1.5
            orientation: 'vertical'
            Label:
                size_hint: 1,None
                height: "20dp"
                text: "Comments:"
                text_size: self.size
                halign: 'justify'
                valign: 'top'
                italic: True
            TextInput:
                id: comment_input
                text: "" if root.task_dict == {} else str(root.task_dict['task_comment'])
        StackLayout:
            size_hint: 1, None
            height: "50dp"
            orientation: 'rl-bt'
            Button:
                size_hint: None, None
                size: ('100dp','40dp')
                text: "Ok"
                on_release: root.change_task()
            Button:
                size_hint: None, None
                size: ("100dp","40dp")
                text: "Cancel"
                on_release: root.dismiss()

########################### End of Task Edit Window ###########################

######################## Beginning of Ress Edit Window ########################

<Ressource_Edit_Window>:
    name_input: name_input
    # ress_group_input: ress_group_input
    box_containing_ressourcegroup: box
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            StackLayout:
                size_hint: 2, 1
                padding: "10dp"
                orientation: 'tb-rl'
                BoxLayout:
                    size_hint: 1, None
                    height: "30dp"

                    Label:
                        size_hint: None, 1
                        width: "50dp"
                        text: "Ressource: "
                        text_size: self.size
                        valign: 'middle'
                        italic: True
                    TextInput:
                        id: name_input
                        text: "" if root.ressource_dict == {} else str(root.ressource_dict['ressource_name'])
            StackLayout:
                size_hint: 1.3, 1
                padding: "10dp"
                orientation: 'tb-rl'
                BoxLayout:
                    id: box
                    size_hint: 1, None
                    height: "30dp"
                    Label:
                        text: "Group: "
                        size_hint: None, 1
                        width: "150dp"
                        text_size: self.size
                        valign: 'middle'
                        italic: True
                    # TextInput:
                    #     id: ress_group_input
                    #     text:  "" if root.ressource_dict == {} else str(root.ressource_dict['ressource_group'])

        StackLayout:
            size_hint: 1, None
            height: "50dp"
            orientation: 'rl-bt'
            Button:
                size_hint: None, None
                size: ('100dp','40dp')
                text: "Ok"
                on_release: root.change_ressource()
            Button:
                size_hint: None, None
                size: ("100dp","40dp")
                text: "Cancel"
                on_release: root.dismiss()

########################### End of Ress Edit Window ###########################
''')


class Task_Edit_Window(Popup):

    # dictionary containing the task's attr
    task_dict = DictProperty({})

    # Objects of the task edit window displaying the task attr
    start_day_input = ObjectProperty(None)
    name_input = ObjectProperty(None)
    duration_input = ObjectProperty(None)
    comment_input = ObjectProperty(None)
    taskgroup_label = ObjectProperty(None)
    box_containing_taskgroup = ObjectProperty()
    # color_box = ObjectProperty()

    def __init__(self, project, task_id = -1, ressource_id = 1, **kwargs):
        super(Task_Edit_Window, self).__init__(**kwargs)

        # Init of the project
        self.project = project

        self.task_id = task_id

        if task_id == -1:
            self.task_dict = {
                    'task_name': "new_task",
                    "ressource_id": ressource_id,
                    'task_row': 0,
                    'task_days': 1,
                    'task_start': "2015-09-01",
                    'task_comment': '',
                    'task_group_id': 1
                        }
        else:
            self.task_dict = {
                    'task_name': self.get_task_attr('task_name'),
                    "ressource_id": self.get_task_attr('ressource_id'),
                    'task_row': self.get_task_attr('task_row'),
                    'task_days': self.get_task_attr('task_days'),
                    'task_start': self.get_task_attr('task_start'),
                    'task_comment': self.get_task_attr('task_comment'),
                    'task_group_id': self.get_task_attr('task_group_id')
                        }

        self.taskgroup_btn = DtbObjctDropDown(
                        linked_dataframe = self.project.taskgroups_dataframe,
                        objct_id = self.task_dict['task_group_id'],
                        attr_displayed_list = ['taskgroup_name'],
                        attr_backcolor = [
                                            'taskgroup_r',
                                            'taskgroup_g',
                                            'taskgroup_b'
                                         ],
                        size_hint = (None,None),
                        size = (100,30)
                                             )
        self.box_containing_taskgroup.add_widget(self.taskgroup_btn)


    def get_task_attr(self, attr):
    # this method get the task attr in the dtf
        return self.project.tasks_dataframe.loc[self.task_id, attr]


    def change_task(self):
    # WHen the ok button is pressed, we need to update the object.

        # If this is a creation of a task then
        if self.task_id == -1:
            # we get the highest index in the tasks_dtf and + 1
            self.task_id = max(self.project.tasks_dataframe.index) + 1

        else:
            # If it's a modification of a task
            # We delete the current task object
            self.project.gant_scrollview.delete_task(
                                task_id = self.task_id,
                                ressource_id = self.task_dict["ressource_id"]
                                                    )

        # we then edit/add the object with the task with the id we want
        # in the dtf
        task = pd.Series({
                        'task_name': self.name_input.text,
                        'ressource_id': int(
                                    self.task_dict["ressource_id"]
                                           ),
                        'task_row': 0,
                        'task_days': int(self.duration_input.text),
                        'task_start': self.start_day_input.text,
                        'task_comment': self.comment_input.text,
                        'task_group_id': self.taskgroup_btn.objct_id
                          }, name = self.task_id
                        )

        self.project.add_task(task = task)

        # the window dismisses
        self.dismiss()


class Ressource_Edit_Window(Popup):

    # dictionary containing the task's attr
    ressource_dict = DictProperty({})

    # Objects of the Ressource edit window displaying the ressource attr
    name_input = ObjectProperty(None)
    # ress_group_input = ObjectProperty(None)
    box_containing_ressourcegroup = ObjectProperty()

    def __init__(self, project, ressource_id = -1, **kwargs):
        super(Ressource_Edit_Window, self).__init__(**kwargs)

        # Init of the project
        self.project = project

        # if ressource_id = -1:
        # Init of the project
        self.ressource_id = ressource_id

        # if it is a creation of a ressource
        if ressource_id == -1:
            self.ressource_dict = {
                    "ressource_name": "new_ressource",
                    "ressource_group_id": 1,
                    "ressource_row": 3,
                    "ressource_place_id": 1
                            }
        # else if it is a modification
        else:
            self.ressource_dict = {
                "ressource_name": self.get_ress_attr("ressource_name"),
                "ressource_group_id": self.get_ress_attr("ressource_group_id"),
                "ressource_row": self.get_ress_attr("ressource_row"),
                "ressource_place_id": self.get_ress_attr("ressource_place_id")
                                  }

        self.ressourcegroup_btn = DtbObjctDropDown(
                    linked_dataframe = self.project.ressourcegroups_dataframe,
                    objct_id = self.ressource_dict['ressource_group_id'],
                    attr_displayed_list = ['ressourcegroup_name'],
                    attr_backcolor = [
                                        'ressourcegroup_r',
                                        'ressourcegroup_g',
                                        'ressourcegroup_b'
                                     ],
                    size_hint = (None,None),
                    size = (100,30)
                                             )
        self.box_containing_ressourcegroup.add_widget(self.ressourcegroup_btn)


    def get_ress_attr(self, attr):
    # this method get the task attr in the dtf
        return self.project.ressources_dataframe.loc[self.ressource_id, attr]


    def change_ressource(self):
    # WHen the ok button is pressed, we need to update the object.

        # If this is a creation of a ress then
        if self.ressource_id == -1:
            # we get the highest index in the ressources_dtf and + 1
            self.ressource_id = (
                                max(self.project.ressources_dataframe.index)
                                + 1
                                )

            ressource = pd.Series({
                'ressource_name': self.name_input.text,
                'ressource_group_id': int(self.ressourcegroup_btn.objct_id),
                'ressource_row': 2,
                "ressource_place_id": 1
                                  }, name = self.ressource_id
                                 )

            self.project.add_ressource(ressource)

        # If it's a modification of a ressource
        else:
        # we then edit the object
            ressource = pd.Series({
                'ressource_name': self.name_input.text,
                'ressource_group_id': int(self.ressourcegroup_btn.objct_id),
                'ressource_row': self.ressource_dict['ressource_row'],
                "ressource_place_id": self.ressource_dict['ressource_place_id']
                                  }, name = self.ressource_id
                                 )

            self.project.update_ressource(ressource)

        # the window dismisses
        self.dismiss()


class TaskGroup_Edit_Window(Popup):

    # dictionary containing the taskgroup's attr
    taskgroup_dict = DictProperty({})
    #
    # # Objects of the taskgroup edit window displaying the taskgroup attr
    # name_input = ObjectProperty(None)

    def __init__(self, project, taskgroup_id = -1, **kwargs):
        super(TaskGroup_Edit_Window, self).__init__(**kwargs)

        # Init of the project
        self.project = project

        # init of the task group id
        self.taskgroup_id = taskgroup_id

        # if it is a creation of a task group
        if taskgroup_id == -1:
            self.taskgroup_dict = {
                    'taskgroup_name': "new_taskgroup",
                    'taskgroup_r': 0,
                    'taskgroup_g': 0,
                    'taskgroup_b': 0,
                                  }
        # If it is a modification
        else:
            self.taskgroup_dict = {
                'taskgroup_name': self.get_taskgroup_attr('taskgroup_name'),
                'taskgroup_r': self.get_taskgroup_attr('taskgroup_r'),
                'taskgroup_g': self.get_taskgroup_attr('taskgroup_g'),
                'taskgroup_b': self.get_taskgroup_attr('taskgroup_b')
                        }

        # We create a color wheel
        self.CPbx =  ColorPickerBox(popupwindow = self)
        # and add it to the edit winodws
        self.add_widget(self.CPbx)
        # and we create register the input for the name of the group which is
        # inside the colorwheel objct
        self.name_input = self.CPbx.gpi

    def get_taskgroup_attr(self, attr):
    # this method get the taskgroup attr in the dtf
        return self.project.taskgroups_dataframe.loc[self.taskgroup_id, attr]


    def change_group(self):
    # WHen the ok button is pressed, we need to update the object.

        # If this is a creation of a taskgroup then
        if self.taskgroup_id == -1:
            # we get the highest index in the taskgroups_dtf and + 1
            self.taskgroup_id = (
                        max(self.project.taskgroups_dataframe.index) + 1
                                )
        else:
            pass

        # building of the new/updated taskgroup according to the input
        taskgroup = pd.Series({
                        'taskgroup_name': self.name_input.text,
                        'taskgroup_r': self.name_input.background_color[0],
                        'taskgroup_g': self.name_input.background_color[1],
                        'taskgroup_b': self.name_input.background_color[2]
                         }, name = self.taskgroup_id
                        )

        # we add/update the taskgroup inside the project dataframe
        self.project.add_taskgroup(taskgroup = taskgroup)

        # the window dismisses
        self.dismiss()


class RessourceGroup_Edit_Window(Popup):

    # dictionary containing the ressourcegroup's attr
    ressourcegroup_dict = DictProperty({})

    def __init__(self, project, ressourcegroup_id = -1, **kwargs):
        super(RessourceGroup_Edit_Window, self).__init__(**kwargs)

        # Init of the project
        self.project = project

        # init of the ressource group id
        self.ressourcegroup_id = ressourcegroup_id

        # if it is a creation of a ressource group
        if ressourcegroup_id == -1:
            self.ressourcegroup_dict = {
                    'ressourcegroup_name': "new_ressourcegroup",
                    'ressourcegroup_r': 0,
                    'ressourcegroup_g': 0,
                    'ressourcegroup_b': 0,
                                  }
        # If it is a modification
        else:
            self.ressourcegroup_dict = {
        'ressourcegroup_name': self.get_ressourcegroup_attr(
                                                    'ressourcegroup_name'
                                                           ),
        'ressourcegroup_r': self.get_ressourcegroup_attr(
                                                    'ressourcegroup_r'
                                                           ),
        'ressourcegroup_g': self.get_ressourcegroup_attr(
                                                    'ressourcegroup_g'
                                                           ),
        'ressourcegroup_b': self.get_ressourcegroup_attr(
                                                    'ressourcegroup_b'
                                                           )
                        }

        # We create a color wheel
        self.CPbx =  ColorPickerBox(popupwindow = self)
        # and add it to the edit winodws
        self.add_widget(self.CPbx)
        # and we create register the input for the name of the group which is
        # inside the colorwheel objct
        self.name_input = self.CPbx.gpi

    def get_ressourcegroup_attr(self, attr):
    # this method get the ressourcegroup attr in the dtf
        return self.project.ressourcegroups_dataframe.loc[
                                                    self.ressourcegroup_id,
                                                    attr
                                                         ]


    def change_group(self):
    # WHen the ok button is pressed, we need to update the object.

        # If this is a creation of a ressourcegroup then
        if self.ressourcegroup_id == -1:
            # we get the highest index in the ressourcegroups_dtf and + 1
            self.ressourcegroup_id = (
                        max(self.project.ressourcegroups_dataframe.index) + 1
                                )
        else:
            pass

        # building of the new/updated ressourcegroup according to the input
        ressourcegroup = pd.Series({
                    'ressourcegroup_name': self.name_input.text,
                    'ressourcegroup_r': self.name_input.background_color[0],
                    'ressourcegroup_g': self.name_input.background_color[1],
                    'ressourcegroup_b': self.name_input.background_color[2]
                                   }, name = self.ressourcegroup_id
                                  )

        # we add/update the ressourcegroup inside the project dataframe
        self.project.add_ressourcegroup(ressourcegroup = ressourcegroup)

        # the window dismisses
        self.dismiss()
