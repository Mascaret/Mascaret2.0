# Kivy libs import

# Python libs import

# Personal libs import

#Class of a task
class Service:

    # columns used in the csv, in the right order
    _dtb_columns = ["service_id", "service_name", "location_id"]
    # name of the dtb table for this object
    _dtb_table = "services"
    # Object(s) which must be included in this object
    _parent_objct = []