# Kivy libs import
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.properties import NumericProperty, ListProperty

# Python libs import

# Personal libs import

class DtbObjctDPbutton(Button):
# This is a button object designed to display any dtb object we want
# It must have one dataframe to look in, and one objct id.
# It can have a list of attr to display and a list of color attr

    # Builder
    def __init__(self, linked_dataframe,
                objct_id,
                attr_displayed_list = [],
                attr_backcolor = [],
                **kwargs):
        super(DtbObjctDPbutton, self).__init__( **kwargs)

        # Init of the dataframe
        self.linked_dataframe = linked_dataframe
        # Init of the ojct_id
        self.objct_id = int(objct_id)
        # Init of the attr to display in the text
        self.attr_displayed_list = attr_displayed_list
        # Init f the attr containing the backcolor info
        self.attr_backcolor = attr_backcolor

        # We launch the drawing method
        self.draw_myself()

    def get_objct_attr(self, attr):
    # this method get the object attr in the dtf
        return self.linked_dataframe.loc[self.objct_id, attr]

    def new_objct_id(self, objct_id):
    # When we want to change the object shown by the button
        self.objct_id = objct_id
        self.draw_myself()

    def draw_myself(self):
    # Method drawing the button
        # Init of the displayed text.
        self.text = ''
        # If an attribute containing text to display has be passed
        if self.attr_displayed_list != []:
            # We loop in the list of attr containing text t diplay
            for attr in self.attr_displayed_list:
                self.text = self.text + ' ' + str(self.get_objct_attr(
                                                                attr = attr
                                                                     ))

        # If attr containing info on the color of the button have been passed
        if self.attr_backcolor != []:
            # We delete the grey background image which would corrupt the
            # color
            self.background_normal = ''
            # We define the color of th text
            self.color = [0,0,0,1]
            # And the bckground color
            self.background_color = [
                        self.get_objct_attr(attr = self.attr_backcolor[0]),
                        self.get_objct_attr(attr = self.attr_backcolor[1]),
                        self.get_objct_attr(attr = self.attr_backcolor[2]),
                        1
                                    ]

class DtbObjctDropDown(DtbObjctDPbutton):
# Class of a DtbObjctDPbutton triggering a dropdown list on_release.

    def __init__(self, **kwargs):
        super(DtbObjctDropDown, self).__init__(**kwargs)

        self.create_dropdown()


    def create_dropdown(self):
        self.dropdownlist = DropDown()

        for ix in self.linked_dataframe.index:
        # when adding widgets, we need to specify the height manually
        # (disabling the size_hint_y) so the dropdown can calculate the
        # area it needs.
            btn = DtbObjctDPbutton(
                            linked_dataframe = self.linked_dataframe,
                            objct_id = ix,
                            attr_displayed_list = self.attr_displayed_list,
                            attr_backcolor = self.attr_backcolor,
                            size_hint = (None,None),
                            size = self.size
                                  )

            # for each button, attach a callback that will call the select()
            # method on the dropdown. We'll pass the text of the button as
            # the data of the selection.
            btn.bind(
                    on_release=lambda btn:
                    self.dropdownlist.select(btn.objct_id)
                    )

            # then add the button inside the dropdown
            self.dropdownlist.add_widget(btn)

        # one last thing, listen for the selection in the dropdown list and
        # assign the data to the button text.
        self.dropdownlist.bind(
                                on_select=lambda instance,
                                x: self.new_objct_id(objct_id = x)
                              )


    def on_release(self):
        self.dropdownlist.open(self)
