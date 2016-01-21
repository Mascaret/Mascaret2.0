#Class of an employee
class Employee:

    # columns used in the csv, in the right order
    _dtb_columns = [
                    "employee_index",
                    "employee_name",
                    "employee_surname",
                    "employee_function"
                   ]
    # name of the dtb table for this object
    _dtb_table = "employees"
    # Object(s) which must be included in this object
    _parent_objct = []
