# Kivy libs import

# Python libs import

# Personal libs import

#Class of a task
class AppExercise:

    # columns used in the csv, in the right order
    _dtb_columns = [
                "appexercise_id", "exercise_id",
                "workout_id", "rep_time",
                "rec_time", "series_goal",
                "reps_goal"
                   ]
    # name of the dtb table for this object
    _dtb_table = "appexercises"
    # Object(s) which must be included in this object
    _parent_objct = []
