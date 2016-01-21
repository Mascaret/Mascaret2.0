# Kivy libs import

# Python libs import

# Personal libs import

#Class of a task
class Serie:

    # columns used in the csv, in the right order
    _dtb_columns = [
                "serie_id", "appexercise_id",
                "serie_n", "reps_qty"

                   ]
    # name of the dtb table for this object
    _dtb_table = "series"
    # Object(s) which must be included in this object
    _parent_objct = []
