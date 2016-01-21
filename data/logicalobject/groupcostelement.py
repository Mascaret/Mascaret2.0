#Class of a cost element group
class CostElementGroup:

    # columns used in the csv, in the right order
    _dtb_columns = [
                    "costelementgroup_id",
                    "costelementgroup_name",
                    "classification_id"
                   ]
    # name of the dtb table for this object
    _dtb_table = "groupcostelement"
    # Object(s) which must be included in this object
    _parent_objct = []
