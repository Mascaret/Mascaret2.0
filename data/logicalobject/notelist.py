#Class of a Note
class NoteList:

    # columns used in the csv, in the right order
    _dtb_columns = [
                    "notelist_index",
                    "notelist_name",
                    "notelist_place_id"
                   ]
    # name of the dtb table for this object
    _dtb_table = "notelists"
    # Object(s) which must be included in this object
    _parent_objct = []
