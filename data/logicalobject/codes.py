# Kivy libs import

# Python libs import

# Personal libs import

#Class of a task
class Code:

    # columns used in the csv, in the right order
    _dtb_columns = [
            "code_id",
            "code_code",
            "code_appdate",
            "code_clodate",
            "codetype_id",
            "project_id",
            "location_id",
            "center_id"
                   ]
    # name of the dtb table for this object
    _dtb_table = "codes"
    # Object(s) which must be included in this object
    _parent_objct = []
