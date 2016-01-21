# Kivy libs import
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scatterlayout import ScatterLayout
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button

# Python libs import

# Personnal Libs imports
from ressource.function.numoperation import NumOperation
from gui.widget.hoverclass.hoverclass import HoverBehavior
from config.cursor import Cursor

Builder.load_string('''
########################## Beginning of NoteListItem ##########################

<NoteListItem>:
    id: notelistitem
    notelistheader: notelistheader
    name_label: name_label
    notelistscrollview: notelistscrollview
    notecontaineritem: notecontaineritem
    size_hint: (None, None)
    height: notelistheader.height + notelistscrollview.height + bottom_button.height
    # do_collide_after_children: True
    do_translation: False
    canvas:
        Color:
            rgba: [0.5,0,0,0.5]
        Rectangle:
            size: self.size
            # pos: self.pos
    # pos: {'x': 0, 'y': 0}
    NoteListHeader:
        id: notelistheader
        notelistitem: notelistitem
        size_hint: (1, None)
        height: 50
        pos: (0, root.height - self.height)
        canvas.before:
            Color:
                rgba: [0,0.2,0,1]
            Rectangle:
                size: self.size
                pos: self.pos
        Label:
            id: name_label
            text: ''
    NoteListScrollView:
        id: notelistscrollview
        size_hint: (1, None)
        height: min(notecontaineritem.height, 500)
        scroll_timeout: 10
        scroll_type: ['bars']
        bar_width: "20dp"
        pos: (0, bottom_button.height + notecontaineritem.padd)
        # canvas.before:
        #     Color:
        #         rgba: [0,0.5,0,0.5]
        #     Rectangle:
        #         size: self.size
        #         pos: self.pos
        NoteContainerItem:
            id: notecontaineritem
            notelistitem: root
            notetool: root.notetool
            size_hint: (1, None)
            height: 0
            canvas:
                Color:
                    rgba: [0,0,0.5,0.5]
                Rectangle:
                    size: self.size
                    pos: self.pos
    NewNoteBtn:
        id: bottom_button
        size_hint: (1, None)
        height: 50
        # pos: {'x': 0, 'y': 0}
        # canvas:
        #     Color:
        #         rgba: [0,1,0.1,0,1]
        #     Rectangle:
        #         size: self.size


############################# End of NoteListItem #############################

###################### Beginning of NewPlaceNoteListItem ######################

<NewPlaceNoteListItem>:
    canvas:
        Color:
            rgba: [0,0,1,1]
        Rectangle:
            size: self.size
            pos: self.pos

######################### End of NewPlaceNoteListItem #########################
''')

class NewPlaceNoteListItem(BoxLayout):
    # place_id = NumericProperty()
    # notelist_id = NumericProperty()

    def __init__(self, notelistitem, **kwargs):
        super(NewPlaceNoteListItem, self).__init__(**kwargs)

        self.notelistitem = notelistitem

        self.place_id = notelistitem.place_id

        self.notelist_id = notelistitem.notelist_id

        self.build_GUI()

    def build_GUI(self):
        self.size_hint = (None, None)
        self.size = self.notelistitem.size

        self.x = self.notelistitem.x

        self.top = self.notelistitem.notetool.notelistcontaineritem.top

    def on_place_id(self, widget, value):
        pass

    def on_notelist_id(self, widget, value):
        pass


class NoteListItem(ScatterLayout):

    # the header box of the note list, containing the name label...
    notelistheader = ObjectProperty(None)
    # the label containing the name of the list
    name_label = ObjectProperty(None)
    # the scrollview containing the notes container
    notelistscrollview = ObjectProperty()
    # the notes container.
    notecontaineritem = ObjectProperty(None)
    # the button at th bottom of the note list, enabling to create a new
    # note
    bottom_button = ObjectProperty(None)
    # the note tool, main layout containing everything, parent of the notelist
    # item
    notetool = ObjectProperty(None)

    # builder
    def __init__(self, notelist_id, place_id, notetool, **kwargs):
        super(NoteListItem, self).__init__(**kwargs)
        # init of the note list id
        self.notelist_id = notelist_id
        # ref of the notetool
        self.notetool = notetool

        self.place_id = place_id

        self.move_flag = False
        # Build the graphic int of the NoteList
        self.build_GUI()

    def build_GUI(self):
    # building of the GUI
        self.name_label.text = self.get_notelist_attr("notelist_name")

        self.memx = self.x

    def get_notelist_attr(self, attr):
        return self.notetool.notelists_dataframe.loc[self.notelist_id, attr]

    def add_noteitem(self, noteitem, note_place_id):
        self.notecontaineritem.add_noteitem(noteitem = noteitem, note_place_id = note_place_id)

    def move_noteitem(self):
        self.notecontaineritem.move_noteitem()

    def on_transform_with_touch(self, touch):

        # we check that it's not a noteitem wich is being moved
        if self.do_translation == (False, False):
            # if it is we stop
            return

        super(NoteListItem, self).on_transform_with_touch(touch)
        # this method is triggered when the note item is moved

        # at the first trigger of this method, meaning at the very beginning
        # of the move, we take this scatter out of the note list to be able
        # to move it in the notetool
        if self.move_flag == False:

            # then we add a widget in the container to simulate the
            # position of the notelistitem if the touch is released
            # ref
            self.new_place_notelistitem = NewPlaceNoteListItem(self)
            # add
            self.parent.add_widget(self.new_place_notelistitem)

            self.memx = self.x

            # First we move ourself from the notelist container to the
            # notetool, in order to be able to move ourself in the window
            self.parent.clear_widgets([self])
            # ref
            self.notetool.moving_notelistitem = self
            # add
            self.notetool.add_widget(self)

            # Trigger of the moveflag
            self.move_flag = True

            Cursor().update('grab')
            Cursor().block()

            return

        # get the place_id the closest from the touch in the notetool
        # We get the adress list
        address_list = self.get_x_address_list()

        # Alors pour le comprendre celui la faut s'accrocher...
        # inside_x = self.notetool.notelistcontaineritem.to_widget(
        #                                             self.x, self.y, True
        #                                                         )[0] + Window.width - self.notetool.x
        inside_x = self.notetool.notelistcontaineritem.to_widget(
                                                    self.x, self.y, True
                                                                )[0] + self.notetool.x
        # explanation of the to_widget...:
        # we want the coordinates in the container space, they will
        # be used to compare with the y addresses of the notelistitems
        # inside this container

        print('x dans le ref container: ' + str(self.notetool.notelistcontaineritem.to_widget(
                                                    self.x, self.y, True
                                                                )[0]))
        print('Window.width: ' + str(Window.width))
        print('pos du notetool: ' + str(self.notetool.x))
        print('inside_x : ' + str(inside_x))
        print('###############################################')

        # we get the closest x in the x address list
        theclosest = NumOperation.takeClosest(
                                myList = address_list,
                                myNumber = inside_x
                                             )

        # we get the new id wanted
        new_place_id = theclosest[1] + 1

        # and if the new place id is the same as before we don't want to move.
        if self.new_place_notelistitem.place_id == new_place_id:
            # then we stop
            return

        # we need to delete the new_place_noteitem
        self.notetool.notelistcontaineritem.clear_notelistitem(notelistitem = self.new_place_notelistitem)

        # we increment all the notelistitems place_ids >= to the new item place id
        self.notetool.notelistcontaineritem.increment_place_ids_after(new_place_id)

        # and add it in the new one
        self.notetool.notelistcontaineritem.add_notelistitem(
                                notelistitem = self.new_place_notelistitem,
                                notelist_place_id = new_place_id
                                                            )

        self.memx = inside_x


    def get_x_address_list(self):
        x_address_list = []
        for i in range(len(self.notetool.notelistitems_dict.values())):
            x_address_list.append(
                                    (i+1) * self.notetool.spacing +
                                    i * self.notetool.notelist_width
                                 )
        return x_address_list



class NoteContainerItem(RelativeLayout):
    # the padding
    padd = NumericProperty(10)
    # the note list item, containing this note container
    # init in the kv
    notelistitem = ObjectProperty(None)
    # the note tool, containing everything, init in the kv
    notetool = ObjectProperty(None)

    # builder
    def __init__(self, **kwargs):
        super(NoteContainerItem, self).__init__(**kwargs)
        # # Init of the local note dictionary   => really needed?
        # self.note_dict = {}
        # self.bind(height=self.on_height)
        self.create_adresses_list()
        pass

    # def on_height(self,widget,value):
    #     if hasattr(self, 'notelistitem') and hasattr(self.notelistitem, 'notelistscrollview') and hasattr(self.notelistitem.notelistscrollview, 'height'):
    #         # self.notelistitem.height += value
    #         self.notelistitem.notelistscrollview.height += value

    def height_upd(self, noteitem_place_id, value):
    # method who updates the height of the notecontainer when a note item
    # sees a change in its height. value represent the height change
        # the height of the container changes
        self.height += value
        # the place of the notes above the changing note must move to there
        # new y
        # we begin to loop through the children
        self.notelistitem.top = self.notetool.notelistcontaineritem.top

        for h in self.children:
            # if the note item is above the changing note item, meaning
            # its place_id is <:
            if h.place_id < noteitem_place_id:
                # its y changes
                h.y += value
                h.memy = h.y

        # finally we create a new address list
        self.create_adresses_list()

    def add_noteitem(self, noteitem, note_place_id):
        noteitem_place_id = note_place_id
        # update the height of the container and the pos of the noteitems
        # which have to move to let the place to the new noteitem
        self.height_upd(
                        noteitem_place_id = noteitem_place_id,
                        value = noteitem.height + self.padd
                       )

        # get the corresponding y of the new note item in the container
        highest_inf_place_id = 0
        # we will get the highest place_id inf to the noteitem_place_id
        for place_id in self.place_id_list[:]:
            if place_id < noteitem_place_id and place_id > highest_inf_place_id:
                highest_inf_place_id = place_id
        # the new noteitem will have to calculate its y according to the
        # noteitem owning this place_id
        noteitem_pos = (
            self.address_list[self.place_id_list.index(highest_inf_place_id)] -
            self.padd - noteitem.height
                       )
        noteitem.pos = (0, noteitem_pos)
        noteitem.memy = noteitem_pos
        noteitem.place_id = note_place_id

        # add the  graphic object
        self.add_widget(noteitem)

        # Creation of the list of the y of the contained headers
        self.create_adresses_list()


    def clear_noteitem(self, noteitem):
        pass
        if not noteitem in self.children:
            return

        # clear the graphic object
        self.clear_widgets([noteitem])

        # update the height of the container and the pos of the noteitems
        # which have to move to take the place of the disappearing noteitem
        self.height_upd(
                        noteitem_place_id = noteitem.place_id,
                        value = - noteitem.height - self.padd
                       )
        # we decrement the place_ids after the place id which is disappearing
        self.decrement_place_ids_after(noteitem.place_id)
        # Creation of the list of the y of the contained headers
        self.create_adresses_list()

    def increment_place_ids_after(self, place_id):
        # increment all the >= place_ids
        for noteitem in self.children:
            if hasattr(noteitem, 'note_id') and noteitem.place_id >= place_id:
                noteitem.place_id += 1

    def decrement_place_ids_after(self, place_id):
        # decrement all the >= place_ids
        for noteitem in self.children:
            if hasattr(noteitem, 'note_id') and noteitem.place_id >= place_id:
                noteitem.place_id -= 1

    def get_note_attr(self, note_id, attr):
    # Method to get the required attr in the ressource dtf
        return self.notetool.notes_dataframe.loc[note_id, attr]

    def get_noteitem(self, note_id):
    # This method get a header from the ressource dict
        # Check if this header exists
        return self.notetool.get_noteitem(note_id)

    def create_adresses_list(self):
    # This method updates the y adress list of the noteitems contained in the
    # header container
        # init
        self.address_list = []
        self.place_id_list = []
        # Begin the loop through all the headers
        for noteitem in self.children:
            # If it is really a header
            if hasattr(noteitem, 'place_id'):
                # then we get its y
                self.address_list.append(noteitem.y)
                self.place_id_list.append(noteitem.place_id)
        # And we add the top of the header container in the list
        self.address_list.append(self.height)
        self.place_id_list.append(0)
        # We finish with a sort
        self.address_list.sort()
        self.place_id_list.sort(reverse = True)

class NoteListScrollView(ScrollView):
    pass

class NewNoteBtn(Button):
    pass

class NoteListHeader(BoxLayout, HoverBehavior):

    notelistitem = ObjectProperty(None)

    def on_enter(self):
        self.notelistitem.do_translation = True
        Cursor().update('hand')

    def on_leave(self):
        if self.notelistitem.move_flag == False:
            self.notelistitem.do_translation = False
            Cursor().update()
