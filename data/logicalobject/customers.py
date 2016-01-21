# Kivy libs import

# Python libs import

# Personal libs import

#Class of a task
class Customer:

    # columns used in the csv, in the right order
    _dtb_columns = ["customer_id", "customer_name", "address_id"]
    # name of the dtb table for this object
    _dtb_table = "customers"
    # Object(s) which must be included in this object
    _parent_objct = []
