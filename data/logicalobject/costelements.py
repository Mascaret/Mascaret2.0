# Kivy libs import

# Python libs import

# Personal libs import

#Class of a task
class CostElement:

    # columns used in the csv, in the right order
    _dtb_columns = [
            "costelement_id", "costelement_code",
            "costelement_desc"
                   ]
    # name of the dtb table for this object
    _dtb_table = "costelements"
    # Object(s) which must be included in this object
    _parent_objct = []
