# Kivy libs import

# Python libs import

# Personal libs import

#Class of a task
class Training:

    # columns used in the csv, in the right order
    _dtb_columns = [
                "training_id", "training_name",
                "training_type", "training_fav"
                   ]
    # name of the dtb table for this object
    _dtb_table = "trainings"
    # Object(s) which must be included in this object
    _parent_objct = []
