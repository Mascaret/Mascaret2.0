# Kivy libs import
from kivy.lang import Builder
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.effects.scroll import ScrollEffect
from kivy.properties import NumericProperty, ListProperty, ObjectProperty
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout

# Python ibs import
from datetime import date, timedelta

# Personal libs import
from ressource.function.calendartools import *


Builder.load_string('''
########################## Beginning of Calendar Items ########################

<CalendarHeaderItem>:
    # The display of one day in the calendarscroll
    # the width is defined by the parent when it's created (parent width / number
    # of days), the height is the width of the parent
    size_hint: (None,1)
    # the day color change according to the day : Sat & Sun !=
    canvas:
        Color:
            rgba:
                ((226/255,228/255,230/255,1) if root.weekday < 5
                else (126/255,128/255,130/255,1))
        Rectangle:
            size: self.size
            pos: self.pos
    # The date is displayed in a label
    Label:
        bold: True
        color: 77/255,77/255,77/255,1
        text: root.day

############################ End of Calendar Items ############################
''')


class CalendarHeaderScroll(ScrollView):
# Class of a horizontal scrollview displaying the days within a period of time

    # Project linked to this calendarScroll. The project
    # gathers the different scrollviews in one single object.
    project = ObjectProperty(None)

    # Builder:
    def __init__(self, project, **kwargs):       #, project
        super(CalendarHeaderScroll, self).__init__( **kwargs)

        # The project gathering the different scrollview in one tool
        self.project = project

        # init of the GUI
        self.build_GUI()


    def days_list_upd(self):
    # When the list of days to display changes, the display is updated

        # By first clearing the current date objects
        self.Calendar_Container.clear_widgets()

        # We update the container width
        self.Calendar_Container.width = (
                                        self.project.day_width *
                                        self.project.number_of_days
                                        )

        for day in self.project.days_dataframe.date:
            # We create 1 object for this date
            day_object = CalendarHeaderItem(day=day)

            day_object.width = self.project.day_width

            self.Calendar_Container.add_widget(day_object)


    def day_width_upd(self):
        # When the width of one day change

        # We update the container width
        self.Calendar_Container.width = (
                                        self.project.day_width *
                                        self.project.number_of_days
                                        )

        # We update the width of the date objects
        for child in self.Calendar_Container.children:
            child.width = self.project.day_width

    def build_GUI(self):
        # We define the way the scroll works.
        # self.scroll_timeout = 10
        self.effect_cls = ScrollEffect

        # To disable scrollin in the CalendarHeaderItem, = "0dp"
        self.bar_width = "0dp"
        self.scroll_type = ['bars'] #bars content

        # We define the "calendar_container" which is the layout insaide the
        # scrollview, containing the dates objects
        self.Calendar_Container = StackLayout()
        self.Calendar_Container.size_hint = None, 1
        self.Calendar_Container.orientation = 'lr-tb'
        self.Calendar_Container.spacing = 0
        self.add_widget(self.Calendar_Container)


class CalendarHeaderItem(BoxLayout):
    day = StringProperty()

    weekday = NumericProperty()

    def on_day(self, widget, day):
        self.weekday = get_date_from_ISO(day).weekday()
