# Kivy libs import

# Python libs import

# Personal libs import

#Class of a task
class ExerciseScaling:

    # columns used in the csv, in the right order
    _dtb_columns = [
                "exercisescaling_id", "exercise_id",
                "exercisescaling_rq",
                "series_scalingrule", "series_max",
                "series_min",
                "reps_scalingrule", "reps_max",
                "reps_min",
                "series_reps_priority",
                "rec_time", "rep_time"
                   ]
    # name of the dtb table for this object
    _dtb_table = "exercisescalings"
    # Object(s) which must be included in this object
    _parent_objct = []
