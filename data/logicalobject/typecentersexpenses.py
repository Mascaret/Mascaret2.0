# Kivy libs import

# Python libs import

# Personal libs import

#Class of a task
class TypeCenterExpense:

    # columns used in the csv, in the right order
    _dtb_columns = [
            "tce_id", "tce_type",
            "center_id"
                   ]
    # name of the dtb table for this object
    _dtb_table = "typecentersexpenses"
    # Object(s) which must be included in this object
    _parent_objct = []
