# Kivy libs import
from kivy.lang import Builder
from kivy.uix.stacklayout import StackLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.effects.scroll import ScrollEffect
from kivy.properties import  ObjectProperty, ListProperty, NumericProperty
from kivy.uix.button import Button
# Python libs import

# Personal libs import
from ressource.function.numoperation import NumOperation
from gui.widget.editwindows import Ressource_Edit_Window
from gui.widget.hoverclass.hoverclass import HoverBehavior
from gui.widget.hoverclass.hoverlabel import HoverLabel1


Builder.load_string('''
########################## Beginning of Header Items ##########################

<HeaderItem>:
    ressource_name_label: ressource_name_label
    # the background of one Header Item
    canvas:
        Color:
            rgba: 226/255,228/255,230/255,1
        Rectangle:
            size: (self.width - 5, self.height)
            pos: ( 5 , 0)
        # Change the color for the drawing of the border lines
        Color:
            rgba: root.ressource_group_color   #226/255,228/255,230/255,1
        # the line surrounding the form, so it has a smooth shape
        Line:
            points:
                (self.width,-2,5,-2,5,
                self.height+2,self.width,self.height+2)
            width: 4
            joint: 'round'
    # the label of the item
    HoverLabel1:
        id: ressource_name_label
        bold: True
        color: 77/255,77/255,77/255,1
        # As soon as the object has a ressource, i's label displays the
        # ressource name (which is in ressource[0])
        text: ""
    NewTaskButton:
        size_hint: None, None
        size: 20,20
        background_normal: 'gui/sharedpics/plus3.png'
        background_color: [0,0,0,0.3]
        pos: (root.width - 30, root.height - 30)
        on_release: root.new_task()

############################# End of Header Items #############################

############################ Beginning of MovLine #############################

<MovLine>:
    size_hint: 1,None
    height: '3dp'
    canvas:
        Color:
            rgba: [1,0,0,1]
        Rectangle:
            size: self.size
            pos: self.pos

############################### End of MovLine ################################
''')



class NewTaskButton(HoverBehavior, Button):

    def on_enter(self):
        self.background_color =  [0,0,0,0.8]

    def on_leave(self):
        self.background_color = [0,0,0,0.3]


class MovLine(BoxLayout):
    pass


class HeaderLabel(HoverLabel1):
    pass


class HeaderItem(ScatterLayout):

    # The label displaying the ressource name
    ressource_name_label = ObjectProperty()

    # The color of the group of thes ressource
    ressource_group_color = ListProperty([0,0,0,1])

    # the header has a place in the header container
    # 1 meaning it is at the top.
    # place_id = NumericProperty(-1)

    # Constructeur
    def __init__(self, ressource_id, project, parnt, place_id, **kwargs):
        super(HeaderItem, self).__init__(**kwargs)

        # Ressource displayed by this object - objet de classe Ressource
        # Init of the ressource
        self.ressource_id = ressource_id
        # self.label.text = ressource.ressource_name

        # This is the position of the header in the  header container
        self.place_id = int(place_id)

        # This attr help to make a bridge with the header container
        self.parnt = parnt

        # Init of the project
        self.project = project

        # this is a flag triggered when the header is moved by touch
        self.move_flag = False

        # init of the GUI
        self.build_UI()


        self.height_mem = self.height
        self.bind(height=self.on_height)
        # Window.bind(mouse_pos=self.on_mouse_pos)

        self.bind(y=self.on_y)

    def on_y(self,widget,values):
    # when the y pos of the header changes, we update the y pos of
    # the linked task area
        if self.ressource_id in self.project.gant_scrollview.ressource_items_dict.keys():
            self.project.gant_scrollview.ressource_items_dict[self.ressource_id].y = self.y

    def on_height(self,widget, value):
    # when the height of the header changes, we update the height of
    # the header container
        self.parnt.height_upd(header = self, value = value - self.height_mem)
        self.height_mem = value

    def build_UI(self):
    # init of the GUI
        self.size_hint = (1, None)
        self.do_translation_x = False

        self.name_update()

        self.upd_color()

    def ressource_updated(self):
        self.name_update()
        self.upd_color()
        self.upd_place_id()

    def name_update(self):
        self.ressource_name_label.text = self.get_ress_attr('ressource_name')

    def upd_place_id(self):
        self.place_id = self.get_ress_attr('ressource_place_id')

    def update_ress_attr_in_dtf(self, attr, value):
    # Method to change the wanted attr in the general ressource dtf
        self.project.ressources_dataframe.loc[self.ressource_id, attr] = value

    def get_ress_attr(self, attr):
    # Method to get the required attr in the ressource dtf
        return self.project.ressources_dataframe.loc[self.ressource_id, attr]

    def upd_color(self):
        ressourcegroup_id = self.get_ress_attr('ressource_group_id')
        self.ressource_group_color = [
            self.project.ressourcegroups_dataframe.loc[
                                                        ressourcegroup_id,
                                                        'ressourcegroup_r'
                                                      ],
            self.project.ressourcegroups_dataframe.loc[
                                                        ressourcegroup_id,
                                                        'ressourcegroup_g'
                                                      ],
            self.project.ressourcegroups_dataframe.loc[
                                                        ressourcegroup_id,
                                                        'ressourcegroup_b'
                                                      ],
            1
                                ]

    def on_touch_down(self, touch, *args):
        super(HeaderItem,self).on_touch_down(touch,*args)
    # This method triggers when the task object is touched by a click
        # If the mouse cursor is on the task object when the click occurs then
        if self.collide_point(touch.x,touch.y):
            # If it's a double click
            if touch.is_double_tap:
                # we create a 'task edit window'
                REW = Ressource_Edit_Window(
                                title = self.get_ress_attr('ressource_name'),
                                project = self.project,
                                ressource_id = self.ressource_id,
                                size_hint = (None, None),
                                size = (700, 200)
                                      )
                # and display it
                REW.open()



    def on_transform_with_touch(self, touch):
        super(HeaderItem, self).on_transform_with_touch(touch)
        # this method is triggered when the header is moved

        # Trigger of the moveflag
        self.move_flag = True

        # We get the list of possible new position for the header
        address_list = self.parnt.address_list[:]
        my_id_in_list = self.parnt.place_id_list.index(self.place_id)
        # and we delete the actual one inside the list
        del address_list[my_id_in_list]

        # we add a colored line in the header container to display the
        # new position of the header if the touch is released
        self.parnt.add_movline()

        # we get the closest y in the y address list
        theclosest = NumOperation.takeClosest(
                                myList = address_list,
                                myNumber = touch.y
                                                )
        # And we move the moveline to this y
        self.parnt.movline.y =  theclosest[0] - self.parnt.padd/2

    def new_task(self):
        self.project.new_task(ressource_id = self.ressource_id)


class HeaderContainer(RelativeLayout):

    padd = NumericProperty(60)

    def __init__(self, project):
        super(HeaderContainer, self).__init__()

        # init of the project
        self.project = project

        # init of the lower line
        self.last_line = self.height

        # Creation of the list of the y of the contained headers
        self.create_adresses_list()

        self.bind(height=self.on_height)

        self.size_hint = 1, None
        self.height = 0


    def on_height(self,widget,value):
        if hasattr(self, 'project'):
            self.project.gant_scrollview.ressources_Container.height = self.height

    def height_upd(self, header, value):
        self.height += value
        for h in self.children:
            if h.place_id < header.place_id:
                h.y += value

        self.create_adresses_list()


    def get_header(self, header_id):
    # This method get a header from the ressource dict
        # Check if this header exists
        if (
            header_id in
            self.project.header_scrollview.ressource_items_dict.keys()
           ):
        #    If it does then it returns the header
            return (
            self.project.header_scrollview.ressource_items_dict[header_id]
                   )
        # else it returns None
        else:
            return None


    def add_header(self, new_header_id):
        # check that the new header to diplay is not already displayed
        self.get_header(new_header_id)
        # if it is stop
        if self.get_header(new_header_id) != None:
            return

        # get the new_header place_id
        new_header_place_id = (
                    self.get_ress_attr(
                                    ressource_id = new_header_id,
                                    attr = 'ressource_place_id'
                                      )
                               )

        # Create the new_header graphic object
        new_header = HeaderItem(
                                parnt = self,
                                ressource_id = new_header_id,
                                project = self.project,
                                place_id = new_header_place_id
                                # Need to add things here
                               )
        # add this new header in the dict
        self.project.header_scrollview.add_header_in_dict(new_header)

        # increment the height of the header container to contain the new
        # header
        self.height += new_header.height + self.padd

        # every header in the header container which will be above the
        # new header goes up, letting a space for the new header at the right
        # pos
        for h in self.children:
            if h.place_id < new_header_place_id:
                h.y += new_header.height + self.padd

        # get the y of each header in the header container
        self.create_adresses_list()

        # get the correspondng y of the new header in the container
        highest_inf_place_id = 0
        # we will get the highest place_id inf to the new_header_id
        for place_id in self.place_id_list[:]:
            if place_id < new_header_place_id and place_id > highest_inf_place_id:
                highest_inf_place_id = place_id
        # the new header will have to calculate its y according to the
        # header owning this place_id
        new_header_pos = (
            self.address_list[self.place_id_list.index(highest_inf_place_id)] -
            self.padd - new_header.height
                         )
        new_header.pos = (0, new_header_pos)

        # add the  graphic object
        self.add_widget(new_header)

        # Creation of the list of the y of the contained headers
        self.create_adresses_list()

    def increment_place_ids_after(self, header_id):
        # increment all the >= place_ids
        # (for place_id >= header.place_id in
        # project.ressources_dataframe.ressource_place_id)
        # (place_id = place_id + 1)
        list_of_ressources_with_place_id_to_change = (
            self.project.ressources_dataframe[
                self.project.ressources_dataframe.ressource_place_id >=
                self.get_ress_attr(header_id, 'ressource_place_id')
                                             ]
                                                     )
        if not list_of_ressources_with_place_id_to_change.empty:
            for i in list_of_ressources_with_place_id_to_change.index:
                self.project.ressources_dataframe.loc[
                                                i,
                                                'ressource_place_id'
                                                     ] += 1

                # We also update the header
                if self.get_header(i) != None:
                    self.get_header(i).upd_place_id()


    def decrement_place_ids_after(self, header_id):
        # decrement all the >= place_ids
        # (for place_id >= header.place_id in
        # project.ressources_dataframe.ressource_place_id)
        # (place_id = place_id - 1)
        list_of_ressources_with_place_id_to_change = (
            self.project.ressources_dataframe[
                self.project.ressources_dataframe.ressources_place_id >=
                self.get_ress_attr(header_id, 'ressource_place_id')
                                             ]
                                                     )
        if not list_of_ressources_with_place_id_to_change.empty:
            for i in list_of_ressources_with_place_id_to_change.index:
                self.project.ressources_dataframe.loc[
                                                i,
                                                'ressource_place_id'
                                                     ] -= 1

                # We also update the header
                if self.get_header(i) != None:
                    self.get_header(i).upd_place_id()


    def del_header(self, header_id):

        # check that the header to delete is being displayed
        self.get_header(header_id)
        # if it isn't stop
        if self.get_header(header_id) == None:
            return

        # clear the display of the header
        self.clear_widgets(header_to_del)

        # get the header_to_del place_id
        header_to_del_place_id = (
                    self.get_ress_attr(header_id, 'ressource_place_id')
                                 )

        self.height += - new_header.height - self.padd

        # get the list of displayed header with a lower place_id
        if self.project.header_scrollview.ressource_items_dict != {}:
            for h in self.project.header_scrollview.ressource_items_dict.values:
                # if the displayed header has a higher place_id then
                # we have to put it up to fill the free space
                if h.place_id < new_header_id:
                    # put them up, headers.y = headers.y + header_to_del.height
                    # + self.padd
                    h.y = h.y - new_header.height - self.padd

        # del this new header in the dict
        self.project.header_scrollview.del_header_in_dict(header_to_del)

        # self.height += - new_header.height - self.padd

        # Creation of the list of the y of the contained headers
        self.create_adresses_list()


    def get_ress_attr(self, ressource_id, attr):
    # Method to get the required attr in the ressource dtf
        return self.project.ressources_dataframe.loc[ressource_id, attr]


    def get_wanted_id_from_movLine_pos(self):
        return (
            self.place_id_list[
                    self.address_list.index(self.movline.y + self.padd/2)
                              ]
               )
        # Explanation:
        # the adress list contains the y of each header,
        # in a sorted order.
        # the MovLine is placed at the
        # (wanted_y -  self.padd/2)
        # The operation above will give the new place_id
        # of the moved header.



    def on_touch_up(self,touch):
        # Vla le bordelllllllllll
        # The goal is to place the header in the order the guy wants.

        # If one header has been moved, the header container contains a
        # MovLine. If the heaer container contains a MovLine, a header has
        # been moved
        if hasattr(self, 'movline'):
            # We need to find which one, so we begin the browsering
            for header in self.children:
                # If a header has been moved, its 'move_flag' is true
                if hasattr(header, 'move_flag') and header.move_flag == True:
                    # We then need too find the new position the user wants
                    new_id = self.get_wanted_id_from_movLine_pos()
                    # we need to re-place the other headers according to the
                    # move
                    # So we begin to loop
                    for eheader in self.children:
                        # need to take care of the header only
                        # (prevents from working on the MovLine)
                        if hasattr(eheader, 'place_id'):
                            # if the header is concerned by the move
                            # in the case of a move-up
                            if (
                                eheader.place_id < header.place_id and
                                eheader.place_id > new_id
                               ):
                                # We need to move the header down
                                # which means that in the same time its
                                # place_id will increase
                                eheader.place_id = eheader.place_id + 1
                                eheader.y = (
                                                eheader.y -
                                                header.height -
                                                self.padd
                                            )

                            # if the header is concerned by the move
                            # in the case of a move-down
                            elif (
                                eheader.place_id > header.place_id and
                                eheader.place_id <= new_id
                                 ):
                                # We need to move the header up
                                # which means that in the same time its
                                # place_id will decrease
                                eheader.place_id = eheader.place_id - 1
                                eheader.y = (
                                                eheader.y +
                                                header.height +
                                                self.padd
                                            )

                    # If it's a move up
                    if header.place_id > new_id:
                        header.place_id = new_id + 1
                        # the place of the moved header goes up
                        # to the MovLine.y
                        header.y = self.movline.y - header.height - self.padd/2
                    else:
                        header.place_id = new_id
                        # the place of the moved header goes down
                        # to the MovLine.y
                        header.y = self.movline.y + self.padd/2

                    # the header.x is re-init => should be diff than 0
                    header.x = 0
                    # And its move_flag is set to False again => move ended
                    header.move_flag = False

            # we finish with the deletion of the MovLine
            self.del_movline()

            # And we update the header_container adress list
            self.create_adresses_list()


    def create_adresses_list(self):
    # This method updates the y adress list of the headers contained in the
    # header container
        # init
        self.address_list = []
        self.place_id_list = []
        # Begin the loop through all the headers
        for header in self.children:
            # If it is really a header
            if hasattr(header, 'place_id'):
                # then we get its y
                self.address_list.append(header.y)
                self.place_id_list.append(header.place_id)
        # And we add the top of the header container in the list
        self.address_list.append(self.height)
        self.place_id_list.append(0)
        # We finish with a sort
        self.address_list.sort()
        self.place_id_list.sort(reverse = True)
        print(self.place_id_list)
        print(self.address_list)

    def add_movline(self):
    # This method add a colored line in the header container
        # check if the line doesn't exist
        if not hasattr(self, 'movline'):
            # then create it
            self.movline = MovLine()
            self.add_widget(self.movline)

    def del_movline(self):
    # This method delete the colore line
        # check if the line exists
        if hasattr(self, 'movline'):
            # then delete it
            self.clear_widgets([self.movline])
            del self.movline



class HeaderScroll(ScrollView):

    # The gant project linked to this gantmainscroll. The gant project
    # gathers the mainscrollview, the calendarscrollview and the
    # headerscrollview in one single object.
    project = ObjectProperty(None)

    # The height of a row
    row_height = NumericProperty()


    def __init__(self, project, **kwargs):
        super(HeaderScroll, self).__init__(**kwargs)

        # The project gathering the different scrollview in one tool
        self.project = project

        # init of the GUI
        self.build_GUI()

        # init of the dictionnary of objects
        self.ressource_items_dict = {}


    def update_from_scroll(self, *largs):
        super(HeaderScroll, self).update_from_scroll(*largs)

        if self.project.being_scrolled == False:
            # the use of the "being_scrolled" var prevent from a loop between
            # the update_from_scroll method of all the scrollview to occur
            # We define it at true at the beginning so update_from_scroll
            # method of the other scrollview don't trigger back
            self.project.being_scrolled = True

            # The scroll of the header on yaxis triggers a scroll of the gant
            self.project.gant_scrollview.scroll_y = self.scroll_y
            self.project.gant_scrollview.update_from_scroll()

            # enable back the scroll methods of other scrollviews
            self.project.being_scrolled = False

    def add_header_in_dict(self, header):
        self.ressource_items_dict[header.ressource_id] = header

    def del_header_in_dict(self, header):
        del self.ressource_items_dict[header.ressource_id]

    def add_ressource(self, ressource_id):
    # this methode add the ressource item

        self.header_container.add_header(new_header_id = ressource_id)
        # self.ressource_items_dict[ressource_id] = HeaderItem(
        #                                 ressource_id = ressource_id,
        #                                 project = self.project
        #                                                     )
        # self.Header_Container.add_widget(
        #                     self.ressource_items_dict[ressource_id])

    def ressource_updated(self, ressource_id):
    # this methode add the ressource item
        self.ressource_items_dict[ressource_id].ressource_updated()


    def delete_ressource(self, ressource_id):
        # Clear the ressources with the id = ressource_id

        self.header_container.del_header(ressource_id = ressource_id)
        # self.header_container.clear_widgets(
        #                         [self.ressource_items_dict[ressource_id]])
        # del self.ressource_items_dict[ressource_id]

    def hide_all_ressources(self):
        # clear all the displayed ressource items
        self.header_container.clear_widgets()
        self.ressource_items_dict.clear()

    def build_GUI(self):
        # We define the way the scroll works.
        self.scroll_timeout = 10
        self.effect_cls = ScrollEffect
        self.bar_width = "0dp"
        self.scroll_type = ['bars']

        # We define the "ressources_container" which is the layout inside
        # the scrollview, containing the ressource objects
        self.header_container = HeaderContainer( project = self.project)
        # self.header_container.bind(minimum_height=self.header_container.setter('height'))
        # self.header_container.orientation = 'lr-tb'
        # self.header_container.spacing =60
        self.add_widget(self.header_container)
