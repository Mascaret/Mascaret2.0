# Kivy libs import
from kivy.core.window import Window
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scatter import Scatter
from kivy.uix.scatterlayout import ScatterLayout
from kivy.properties import ObjectProperty, ListProperty, NumericProperty
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
# Python libs import
import random

# Personnal Libs imports
from tools.notetool.gui.noteitem import NoteItem
from tools.notetool.gui.notelist import NoteListItem
from ressource.function.numoperation import NumOperation
from data.logicalobject.note import Note
from data.logicalobject.notelist import NoteList
from data.db import MyDB
from config.cursor import Cursor


Builder.load_string('''
############################ Beginning of NoteTool ############################

<NoteTool>:
    notelistcontaineritem: notelistcontaineritem
    # canvas:
    #     Color:
    #         rgba: 1,0,0,0.5
    #     Rectangle:
    #         # pos: self.pos
    #         size: self.size
    Label:
        text: "Notetoooooooooooooooooooooooooooooool"
    NoteToolScrollView:
        size_hint: (1,0.8)
        scroll_timeout: 0
        scroll_type: ['bars']
        bar_width: "30dp"
        NoteListContainerItem:
            id: notelistcontaineritem
            notetool: root
            size_hint: (None, 1)
            width: 0
            canvas:
                Color:
                    rgba: 1,0,0,0.5
                Rectangle:
                    pos: self.pos
                    size: self.size

############################### End of NoteTool ###############################
''')



class NoteListContainerItem(RelativeLayout):

    notetool = ObjectProperty(None)

    spacing = NumericProperty(50)

    def on_height(self, widget, value):
        # super(NoteTool, self).on_size(widget,value)
        # print('heght upd')
        # print(value)
        # print('self.notelistcontaineritem.height: ' + str(self.height))
        if hasattr(self, 'children'):
            for nl in self.children:
                nl.top = self.top
                pass

    def width_upd(self, notelistitem_place_id, value):
    # method who updates the width of the notelistcontainer when a notelistitem
    # is added or deleted
        # the width of the container changes
        self.width += value
        # the place of the notelists right to the changing note must
        # move to there new x
        # we begin to loop through the children
        for nl in self.children:
            # if the notelist item is left to the changing notelistitem,
            # meaning its place_id is <:
            if nl.place_id > notelistitem_place_id:
                # its x changes
                nl.x += value
                nl.memx = nl.x

    def add_notelistitem(self, notelistitem, notelist_place_id):
        notelistitem_place_id = notelist_place_id
        # update the width of the container and the pos of the notelistitems
        # which have to move to let the place to the new notelistitem
        self.width_upd(
                        notelistitem_place_id = notelistitem_place_id,
                        value = notelistitem.width + self.spacing
                       )

        # get the corresponding x of the new notelistitem in the container
        notelistitem_x = (
                    notelist_place_id * self.spacing +
                    (notelist_place_id - 1) * self.notetool.notelist_width
                         )
        notelistitem.x = notelistitem_x
        # notelistitem.y = self.height - notelistitem.height
        # notelistitem.top = self.top
        notelistitem.memx = notelistitem_x
        notelistitem.place_id = notelist_place_id

        # add the  graphic object
        self.add_widget(notelistitem)

        print('tooooooooooooooooooooooooooooooooooooop')


    def clear_notelistitem(self, notelistitem):

        if not notelistitem in self.children:
            return

        # clear the graphic object
        self.clear_widgets([notelistitem])

        # update the width of the container and the pos of the notelistitems
        # which have to move to take the place of the disappearing one
        self.width_upd(
                        notelistitem_place_id = notelistitem.place_id,
                        value = - notelistitem.width - self.spacing
                       )
        # we decrement the place_ids after the place id which is disappearing
        self.decrement_place_ids_after(notelistitem.place_id)


    def increment_place_ids_after(self, place_id):
        # increment all the >= place_ids
        print('the new place id: ' + str(place_id))
        for notelistitem in self.children:
            if hasattr(notelistitem, 'notelist_id') and notelistitem.place_id >= place_id:
                print('inc of the notelist: ' + notelistitem.name_label.text)
                print('actual place id: ' + str(notelistitem.place_id))

                notelistitem.place_id += 1

    def decrement_place_ids_after(self, place_id):
        # decrement all the >= place_ids
        for notelistitem in self.children:
            if hasattr(notelistitem, 'notelist_id') and notelistitem.place_id >= place_id:
                notelistitem.place_id -= 1


class NoteToolScrollView(ScrollView):
    pass




class NoteTool(RelativeLayout):
    notelistcontaineritem = ObjectProperty(None)

    notelist_width = NumericProperty(200)

    spacing = NumericProperty(50)

    def __init__(self, **kwargs):
        super(NoteTool, self).__init__(**kwargs)
        #init of the db
        self.mydb = MyDB()
        # we get the note lists
        self.notelists_dataframe = self.mydb.get_dataframe(objct = NoteList)
        # we build the notelists items
        self.init_notelistitems()

        # we get the notes
        self.notes_dataframe = self.mydb.get_dataframe(objct = Note)
        # we build the note items
        self.init_noteitems()

        self.moving_noteitem = None
        self.moving_notelistitem = None

    def init_notelistitems(self):
        self.notelistitems_dict = {}
        self.i = 0

        for ix in self.notelists_dataframe.index:
            self.add_notelistitem(ix)

    def init_noteitems(self):
        self.noteitems_dict = {}

        for ix in self.notes_dataframe.index:
            self.add_noteitem(ix)

    def add_notelistitem_in_dict(self, notelistitem):
        self.notelistitems_dict[notelistitem.notelist_id] = notelistitem

    def add_noteitem_in_dict(self, noteitem):
        self.noteitems_dict[noteitem.note_id] = noteitem

    def del_notelisttiem_in_dict(self, notelistitem):
        del self.notelistitems_dict[notelistitem.notelist_id]

    def del_noteitem_in_dict(self, noteitem):
        del self.noteitems_dict[noteitem.note_id]

    def add_notelistitem(self, notelist_id):

        # we get the place_id
        place_id = self.get_notelist_attr(
                                            notelist_id = notelist_id,
                                            attr = 'notelist_place_id'
                                     )

        # we create the notelistitem
        new_notelistitem = NoteListItem(
            notelist_id = notelist_id,
            notetool = self,
            place_id = place_id,
            width = self.notelist_width
                                              )
        # we add it to the dict
        self.add_notelistitem_in_dict(notelistitem = new_notelistitem)
        # we display it
        self.notelistcontaineritem.add_notelistitem(notelistitem = new_notelistitem, notelist_place_id = place_id)

    def add_noteitem(self, note_id):

        # we get the notelist_id in wich the note is added
        linked_notelist_id = self.get_note_attr(
                                            note_id = note_id,
                                            attr = 'notelist_index'
                                               )
        # we get the notelistitem
        linked_notelist = self.notelistitems_dict[linked_notelist_id]

        # we get the place_id
        place_id = self.get_note_attr(
                                            note_id = note_id,
                                            attr = 'note_place_id'
                                     )

        # we create the note item
        new_noteitem = NoteItem(
                            note_id = note_id,
                            notetool = self,
                            notecontainer = linked_notelist.notecontaineritem,
                            place_id = place_id,
                            notelist_id = linked_notelist_id
                               )
        # we add it to the dict
        self.add_noteitem_in_dict(noteitem = new_noteitem)

        # we ask the linked notelist to display it
        linked_notelist.add_noteitem(noteitem = new_noteitem, note_place_id = place_id)

    def get_notelistitem(self, notelist_id):
    # This method get a noteitem from the noteitem dict
        # Check if this noteitem exists
        if (
            notelist_id in
            self.notelistitems_dict.keys()
           ):
        #    If it does then it returns the header
            return (
            self.notelistitems_dict[notelist_id]
                   )
        # else it returns None
        else:
            return None

    def get_note_attr(self, note_id, attr):
    # Method to get the required attr in the ressource dtf
        return self.notes_dataframe.loc[note_id, attr]

    def get_notelist_attr(self, notelist_id, attr):
    # Method to get the required attr in the notelist dtf
        return self.notelists_dataframe.loc[notelist_id, attr]

    def get_noteitem(self, note_id):
    # This method get a noteitem from the noteitem dict
        # Check if this noteitem exists
        if (
            note_id in
            self.noteitems_dict.keys()
           ):
        #    If it does then it returns the header
            return (
            self.noteitems_dict[note_id]
                   )
        # else it returns None
        else:
            return None

    def on_touch_up(self,touch):
        # if there is a moving_noteitem in the notetool it mean the touch up is
        # the end of a grab of a noteitem.
        if self.moving_noteitem != None:
            # therfore we need to insert this
            # moving noteitem at the chosen place
            self.insert_moving_noteitem()

        if self.moving_notelistitem != None:
            # therfore we need to insert this
            # moving noteitem at the chosen place
            self.insert_moving_notelistitem()


    def insert_moving_noteitem(self):
    # method to insert a moving noteitem at the place of its new_place_noteitem
        # At first we clear it from the notetool
        self.clear_widgets([self.moving_noteitem])

        # re-ref of the notelistitem
        self.moving_noteitem.notecontainer = self.moving_noteitem.new_place_noteitem.notecontainer
        # re-Init of the place_id
        self.moving_noteitem.place_id = self.moving_noteitem.new_place_noteitem.place_id
        # re-Init of the notelist_id
        self.moving_noteitem.notelist_id = self.moving_noteitem.new_place_noteitem.notelist_id
        # this is a flag triggered when the note item is moved by touch
        self.moving_noteitem.move_flag = False
        # re-Init of the pos
        self.moving_noteitem.pos = self.moving_noteitem.new_place_noteitem.pos

        # We clear the NewPlaceNoteItem from the container
        self.moving_noteitem.new_place_noteitem.notecontainer.clear_widgets(
                                    [self.moving_noteitem.new_place_noteitem]
                                                                       )

        # We add it to the new container
        self.moving_noteitem.new_place_noteitem.notecontainer.add_widget(
                                                    self.moving_noteitem
                                                                    )
        # we delete the NewPlaceNoteItem of the moving noteitem
        del self.moving_noteitem.new_place_noteitem

        # de-ref of the moving note item
        self.moving_noteitem = None

        Cursor().unblock()
        Cursor().update()

    def insert_moving_notelistitem(self):
    # method to insert a moving notelistitem at the place of its new_place_notelistitem
        # At first we clear it from the notetool
        self.clear_widgets([self.moving_notelistitem])

        # re-Init of the place_id
        self.moving_notelistitem.place_id = self.moving_notelistitem.new_place_notelistitem.place_id
        # this is a flag triggered when the note item is moved by touch
        self.moving_notelistitem.move_flag = False
        # re-Init of the pos
        self.moving_notelistitem.pos = self.moving_notelistitem.new_place_notelistitem.pos

        # We clear the NewPlaceNoteListItem from the container
        self.notelistcontaineritem.clear_widgets(
                            [self.moving_notelistitem.new_place_notelistitem]
                                                                       )

        # We add it to the new container
        self.notelistcontaineritem.add_widget(
                                            self.moving_notelistitem
                                             )
        # we delete the NewPlaceNoteItem of the moving noteitem
        del self.moving_notelistitem.new_place_notelistitem

        # de-ref of the moving note item
        self.moving_notelistitem = None

        Cursor().unblock()
        Cursor().update()
