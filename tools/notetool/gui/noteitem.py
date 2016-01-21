# Kivy libs import
from kivy.lang import Builder
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, ListProperty

# Python libs import
import random

# Personnal Libs imports
from ressource.function.numoperation import NumOperation

Builder.load_string('''
############################ Beginning of NoteItem ############################

<NoteItem>:
    desc_label: desc_label
    do_rotation: False
    do_scale: False
    size_hint: (None, None)
    # size: (100,100)
    canvas:
        Color:
            rgba: root.color
        Rectangle:
            size: self.size
    Label:
        id: desc_label
        text: ""

############################### End of NoteItem ###############################

######################## Beginning of NewPlaceNoteItem ########################

<NewPlaceNoteItem>:
    canvas:
        Color:
            rgba: [0,0,1,1]
        Rectangle:
            size: self.size
            pos: self.pos

########################### End of NewPlaceNoteItem ###########################
''')


class NoteItem(ScatterLayout):

    desc_label = ObjectProperty()

    color = ListProperty([0,0,0,1])

    def __init__(self, note_id, notetool, notecontainer, place_id, notelist_id, **kwargs):
        super(NoteItem, self).__init__(**kwargs)
        # Init of th note_id
        self.note_id = note_id
        # Ref of the notetool
        self.notetool = notetool
        # ref of the notelistitem
        self.notecontainer = notecontainer
        # Init of the place_id
        self.place_id = int(place_id)
        # Init of the notelist_id
        self.notelist_id = notelist_id
        # this is a flag triggered when the note item is moved by touch
        self.move_flag = False
        # init of the GUI
        self.build_UI()

    def build_UI(self):
    # init of the GUI
        # block the width to the width of the parent
        # self.size_hint = (1, None)
        self.width = self.notetool.notelist_width

#################################to delete##################################
        self.height = random.randrange(50,150,10)
#################################to delete##################################

        # block the translation on x
        # self.do_translation_x = False
        # self.do_translation_y = False
        # Get the desc of the note in teh noteitem label
        self.name_update()

        self.memy = self.y

    def note_updated(self):
        self.name_update()

    def name_update(self):
    # method triggered to update the label of the noteitem according to the
    # the description of the note in the dtb
        self.desc_label.text = self.get_note_attr("note_description")

    def upd_place_id(self):
        self.place_id = self.get_note_attr('note_place_id')

    def update_note_attr_in_dtf(self, attr, value):
    # Method to change the wanted attr in the general note dtf
        self.notetool.notes_dataframe.loc[self.note_id, attr] = value

    def get_note_attr(self, attr):
    # Method to get the required attr in the note dtf
        return self.notetool.notes_dataframe.loc[self.note_id, attr]

    def on_transform_with_touch(self, touch):
        super(NoteItem, self).on_transform_with_touch(touch)
        # this method is triggered when the note item is moved

        # at the first trigger of this method, meaning at the very beginning
        # of the move, we take this scatter out of the note list to be able
        # to move it in the notetool
        if self.move_flag == False:

            # then we add a widget in the container to simulate the
            # position of the noteitem if the touch is released
            # ref
            self.new_place_noteitem = NewPlaceNoteItem(self)
            # add
            self.notecontainer.add_widget(self.new_place_noteitem)

            self.memy = self.y

            # First we move ourself form the note container to the
            # note tool, in order to be able to move ourself in the window
            self.parent.clear_widgets([self])
            # ref
            self.notetool.moving_noteitem = self
            # add
            self.notetool.add_widget(self)

            # Trigger of the moveflag
            self.move_flag = True

            return
############ Need to detect what is the container hoveredd in here ############
        hovered_container = self.get_hovered_container(touch)
############ Need to detect what is the container hoveredd in here ############

        # get the place_id the closest from the touch in the hovered_container
        # We get the adress list of this container
        address_list = hovered_container.address_list[:]

        inside_y = hovered_container.to_widget(*self.pos)[1]
        # explanation of the to_widget...:
        # we want the coordinates in the container space, they will
        # be used to compare with the y addresses of the noteitems
        # inside this container

        theclosest = NumOperation.takeClosest(
                                myList = address_list,
                                myNumber = inside_y + self.height
                                             )

        # we get the new id wanted
        new_place_id = hovered_container.place_id_list[theclosest[1]] + 1
        # We +1 because if we get "1" as the new_place_id, it means that we
        # want to be AFTER the place_id "1" => place_id "2"

        # if the container which is hovered is the same as before
        if self.new_place_noteitem.notecontainer == hovered_container:
            # and if the new place id is the same as before or the same as
            # before + 1
            # explanation: if the touch indicates that we want to be after
            # ourself or after the one before us. In both cases, it
            # indicates that we don't want to move.
            if self.new_place_noteitem.place_id in [new_place_id]:
                # then we stop
                return
            elif inside_y > self.memy and self.new_place_noteitem.place_id < new_place_id:
                return
            elif inside_y < self.memy and self.new_place_noteitem.place_id > new_place_id:
                return

        # we need to delete the new_place_noteitem from its container
        self.new_place_noteitem.notecontainer.clear_noteitem(noteitem = self.new_place_noteitem)
        # we increment all the noteitem place_ids >= to the new item place id
        hovered_container.increment_place_ids_after(new_place_id)
        # and add it in the new one
        hovered_container.add_noteitem(noteitem = self.new_place_noteitem, note_place_id = new_place_id)

        self.memy = inside_y
        # self.stop = True

        self.new_place_noteitem.notecontainer = hovered_container
        self.new_place_noteitem.notelist_id = hovered_container.notelistitem.notelist_id


    def get_hovered_container(self, touch):
        hovered_container = self.notecontainer
        for notelistitem in self.notetool.notelistitems_dict.values():
            if notelistitem.collide_point(touch.x,touch.y):
                hovered_container = notelistitem.notecontaineritem
                break
        return hovered_container


class NewPlaceNoteItem(BoxLayout):
    # place_id = NumericProperty()
    # notelist_id = NumericProperty()

    def __init__(self, noteitem, **kwargs):
        super(NewPlaceNoteItem, self).__init__(**kwargs)

        self.noteitem = noteitem

        self.place_id = noteitem.place_id

        self.notelist_id = noteitem.notelist_id

        self.notecontainer = noteitem.notecontainer

        self.build_GUI()

    def build_GUI(self):
        self.size_hint = (None, None)
        self.size = self.noteitem.size

        self.y = self.noteitem.memy

        self.x = 0

    def on_place_id(self, widget, value):
        pass

    def on_notelist_id(self, widget, value):
        pass
