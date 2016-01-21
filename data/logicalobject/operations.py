#Class of an operation
class Operation:

    # columns used in the csv, in the right order
    _dtb_columns = [
                    "operation_index",
                    "operation_name"
                   ]
    # name of the dtb table for this object
    _dtb_table = "employees"
    # Object(s) which must be included in this object
    _parent_objct = []

1,Read
2,Write
