#Class of a Note
class Note:

    # columns used in the csv, in the right order
    _dtb_columns = [
                    "note_index",
                    "note_description",
                    "user_index",
                    "note_r",
                    "note_g",
                    "note_b",
                    "notelist_index",
                    "note_place_id"
                   ]
    # name of the dtb table for this object
    _dtb_table = "notes"
    # Object(s) which must be included in this object
    _parent_objct = []
