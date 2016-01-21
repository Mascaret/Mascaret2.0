# Kivy libs import

# Python libs import

# Personal libs import
from data.logicalobject.ressource import Ressource

#Class of a task
class Task:

    # columns used in the csv, in the right order
    _dtb_columns = ["task_id", "task_name", "ressource_id","task_row",
                    "task_days","task_start","task_comment", "task_group_id"]
    # name of the dtb table for this object
    _dtb_table = "Tasks"
    # Object(s) which must be included in this object
    _parent_objct = [(Ressource,"ressource_id")]

    def __init__(self, task_row):
        self.task_index = task_row.name
        self.task_name = task_row["task_name"]
        self.task_row = task_row["task_row"]
        self.task_days = task_row["task_days"]
        self.task_start = task_row["task_start"]

        # the columns "ressource_id" should contain the object, not the id.
        self.ressource_objct = task_row["ressource_id"]
