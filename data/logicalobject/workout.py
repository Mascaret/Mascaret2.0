# Kivy libs import

# Python libs import

# Personal libs import

#Class of a task
class Workout:

    # columns used in the csv, in the right order
    _dtb_columns = [
                "workout_id", "workout_date",
                "workout_n", "training_id"
                   ]
    # name of the dtb table for this object
    _dtb_table = "workouts"
    # Object(s) which must be included in this object
    _parent_objct = []
