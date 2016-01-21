# Kivy libs import

# Python libs import

# Personal libs import

#Class of a task
class WBSElement:

    # columns used in the csv, in the right order
    _dtb_columns = [
            "wbs_id", "code_id",
            "wbsca_id"
                   ]
    # name of the dtb table for this object
    _dtb_table = "wbselements"
    # Object(s) which must be included in this object
    _parent_objct = []
