# Kivy libs import

# Python libs import

# Personal libs import

#Class of a task
class Exercise:

    # columns used in the csv, in the right order
    _dtb_columns = [
                "exercise_id", "exercise_name",
                "exercise_type", "exercise_desc",
                "exercise_image1", "exercise_bg"
                   ]
    # name of the dtb table for this object
    _dtb_table = "exercises"
    # Object(s) which must be included in this object
    _parent_objct = []
