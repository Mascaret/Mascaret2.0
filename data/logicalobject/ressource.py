#Class of a ressource
class Ressource:

    # columns used in the csv, in the right order
    _dtb_columns = [
                    "ressource_index",
                    "ressource_name",
                    "ressource_group_id",
                    "ressource_row",
                    "ressource_place_id"
                   ]
    # name of the dtb table for this object
    _dtb_table = "Ressources"
    # Object(s) which must be included in this object
    _parent_objct = []

    def __init__(self, ressource_row):
        self.ressource_index = ressource_row.name
        self.ressource_name = ressource_row["ressource_name"]
        self.ressource_group = ressource_row["ressource_group"]
        # self.list_tasks = list_tasks
