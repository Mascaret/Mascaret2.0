#Class of a status
class Status:

    # columns used in the csv, in the right order
    _dtb_columns = [
                    "status_id",
                    "status_name"
                   ]
    # name of the dtb table for this object
    _dtb_table = "status"
    # Object(s) which must be included in this object
    _parent_objct = []
