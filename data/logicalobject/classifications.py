#Class of a classification
class Classification:

    # columns used in the csv, in the right order
    _dtb_columns = [
                    "classification_id",
                    "classification_name",
                    "classification_desc"
                   ]
    # name of the dtb table for this object
    _dtb_table = "classifications"
    # Object(s) which must be included in this object
    _parent_objct = []
