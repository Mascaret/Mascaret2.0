# Kivy libs import

# Python libs import

# Personal libs import

#Class of a task
class Address:

    # columns used in the csv, in the right order
    _dtb_columns = [
                "address_id", "street_number",
                "street_type", "street_name",
                "address_zipcode", "address_country",
                "address_city", "customer_id"
                   ]
    # name of the dtb table for this object
    _dtb_table = "address"
    # Object(s) which must be included in this object
    _parent_objct = []
