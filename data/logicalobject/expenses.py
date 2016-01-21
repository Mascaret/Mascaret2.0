# Kivy libs import

# Python libs import

# Personal libs import

#Class of a task
class Expense:

    # columns used in the csv, in the right order
    _dtb_columns = [
            "expense_id",
            "tce_id",
            "status_id",
            "costelement_id",
            "expense_amount",
            "expense_qty",
            "expense_date",
            "expense_comment",
            "wbs_id"
                   ]
    # name of the dtb table for this object
    _dtb_table = "expenses"
    # Object(s) which must be included in this object
    _parent_objct = []
