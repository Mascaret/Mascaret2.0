#Class of a tool
class Tool:

    # columns used in the csv, in the right order
    _dtb_columns = [
                    "tool_index",
                    "module_index",
                    "tool_type_index",
                    "tool_name"
                   ]
    # name of the dtb table for this object
    _dtb_table = "tools"
    # Object(s) which must be included in this object
    _parent_objct = []
