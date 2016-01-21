# association class between users and tools
class UserTool:

    # columns used in the csv, in the right order
    _dtb_columns = [
                    "user_index",
                    "tool_index"
                   ]
    # name of the dtb table for this object
    _dtb_table = "userstools"
    # Object(s) which must be included in this object
    _parent_objct = []
