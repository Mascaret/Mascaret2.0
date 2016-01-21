#Class of a tool type
class ToolType:

    # columns used in the csv, in the right order
    _dtb_columns = [
                    "tool_type_index",
                    "tool_type_name",
                   ]
    # name of the dtb table for this object
    _dtb_table = "tooltypes"
    # Object(s) which must be included in this object
    _parent_objct = []
