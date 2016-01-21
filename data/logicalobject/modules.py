#Class of a module
class Module:

    # columns used in the csv, in the right order
    _dtb_columns = [
                    "module_index",
                    "module_name",
                    "module_wp"
                   ]
    # name of the dtb table for this object
    _dtb_table = "modules"
    # Object(s) which must be included in this object
    _parent_objct = []
