#Class of a user
class Userd:

    # columns used in the csv, in the right order
    _dtb_columns = [
                    "user_index",
                    "employee_index",
                    "user_login",
                    "user_password"
                   ]
    # name of the dtb table for this object
    _dtb_table = "users"
    # Object(s) which must be included in this object
    _parent_objct = []
