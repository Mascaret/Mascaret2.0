# Kivy libs import

# Python libs import

# Personal libs import

#Class of a task
class Center:

    # columns used in the csv, in the right order
    _dtb_columns = [
                "center_id", "center_name",
                "center_desc", "service_id"
                   ]
    # name of the dtb table for this object
    _dtb_table = "centers"
    # Object(s) which must be included in this object
    _parent_objct = []
