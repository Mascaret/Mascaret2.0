# Kivy libs import

# Python libs import

# Personal libs import

#Class of a task
class Project:

    # columns used in the csv, in the right order
    _dtb_columns = [
            "project_id", "project_name",
            "project_appdate", "project_rewdate",
            "project_clodate", "project_editflag",
            "project_enmodification", "projecttype_id",
            "customer_id", "location_id"
                   ]
    # name of the dtb table for this object
    _dtb_table = "projects"
    # Object(s) which must be included in this object
    _parent_objct = []
