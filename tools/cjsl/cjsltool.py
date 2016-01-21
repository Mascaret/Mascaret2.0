# Kivy libs import
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import (
                            NumericProperty, ReferenceListProperty,
                            ObjectProperty, StringProperty,
                            ListProperty, DictProperty
                            )

# Python libs import
import pandas as pd
pd.core.format.header_style = None  # <--- Workaround for header formatting
import subprocess
import shutil

# Personnal Libs imports
from data.logicalobject.expenses import Expense
from data.logicalobject.typecentersexpenses import TypeCenterExpense
from data.logicalobject.centers import Center
from data.logicalobject.services import Service
from data.logicalobject.status import Status
from data.logicalobject.costelements import CostElement
from data.logicalobject.costelementgroupsces import CEGroupCE
from data.logicalobject.groupcostelement import CostElementGroup
from data.logicalobject.classifications import Classification
from data.logicalobject.wbselements import WBSElement
from data.logicalobject.wbsca import WBSCA
from data.logicalobject.codes import Code
from data.logicalobject.codetyp import CodeTyp
from data.logicalobject.projects import Project
from data.logicalobject.projecttypes import ProjectType
from data.logicalobject.locations import Location
from data.logicalobject.customers import Customer
from data.db import MyDB

Builder.load_string('''

''')


class CJSLTool(FloatLayout):

##################### Constructeur #####################
    def __init__(self, **kwargs):
        super(CJSLTool, self).__init__(**kwargs)

        # We build the GUI
        self.build_GUI()

        self.write_dtf_to_csv(self.get_expense_dtf())

        self.launch_cjsl()


    def launch_cjsl(self):

        shutil.copyfile(
        'D:\\Programmation\\Mascaret\\Programme Mascaret 2.0\\tools\\cjsl\\excel\\cjsl.xlsm',
        'D:\\Programmation\\Mascaret\\Programme Mascaret 2.0\\temp\\cjsl.xlsm'
                       )


        p = subprocess.Popen([
            "C:\Program Files\Microsoft Office\Office14\EXCEL.EXE",
            'D:\\Programmation\\Mascaret\\Programme Mascaret 2.0\\temp\\cjsl.xlsm'
                            ])

        # ret_val = p.wait()

        
    def write_dtf_to_csv(self, dtf):

        dtf.to_csv(
        'D:\\Programmation\\Mascaret\\Programme Mascaret 2.0\\temp\\exp.csv',
        index = False
                                 )


    def get_expense_dtf(self):
        #init of the db
        self.mydb = MyDB()

        # we get the expenses
        expenses_dataframe = (
        pd.merge(
            pd.merge(
                pd.merge(
                    pd.merge(
                        self.mydb.get_dataframe(objct = Expense),
                        ################ B TCE DTF ###############
                        pd.merge(
                            self.mydb.get_dataframe(objct = TypeCenterExpense, index = False),
                            pd.merge(
                                self.mydb.get_dataframe(objct = Center, index = False),
                                pd.merge(
                                    self.mydb.get_dataframe(objct = Service, index = False),
                                    self.mydb.get_dataframe(objct = Location, index = False).drop(
                                                                                        'legalentity_id',
                                                                                        axis=1
                                                                                                 ),
                                    on = 'location_id', how = 'left'
                                        ).drop(
                                        'location_id',
                                        axis=1
                                              ),
                                on = 'service_id', how = 'left'
                                    ).drop(
                                    'service_id',
                                    axis=1
                                          ),
                            on = "center_id", how = 'left'
                                ).drop(
                                "center_id",
                                axis=1
                                      ),
                        ################ E TCE DTF ###############
                        on = "tce_id", how = 'left'
                            ).drop(
                            "tce_id",
                            axis=1
                                  ),
                    self.mydb.get_dataframe(objct = Status, index = False),
                    on = 'status_id', how = 'left'
                                            ).drop(
                                            'status_id',
                                            axis=1
                                                  ),
                ################ B COSTELMT DTF ###############
                pd.merge(
                    pd.merge(
                        self.mydb.get_dataframe(objct = CostElement, index = False),
                        self.mydb.get_dataframe(objct = CEGroupCE, index = False),
                        on = 'costelement_id', how = 'left'
                            ),
                    self.mydb.get_dataframe(objct = CostElementGroup, index = False),   # ADD .classification_id == ...
                    on = "costelementgroup_id", how = 'left'
                        ).drop(
                        "costelementgroup_id",
                        axis=1
                              ),
                ################ B COSTELMT DTF ###############
                on = 'costelement_id', how = 'left'
                    ).drop(
                    'costelement_id',
                    axis=1
                          ),
            ################ B WBS DTF ###############
            pd.merge(
                pd.merge(
                    self.mydb.get_dataframe(objct = WBSElement, index = False),
                    ################ B CODE DTF ###############
                    pd.merge(
                        # pd.merge(
                            pd.merge(
                                pd.merge(
                                    self.mydb.get_dataframe(objct = Code, index = False),
                                    self.mydb.get_dataframe(objct = CodeTyp, index = False),
                                    on = 'codetype_id', how = 'left'
                                        ).drop(
                                        'codetype_id',
                                        axis=1
                                              ),
                                ################ B PROJECT DTF ###############
                                pd.merge(
                                    pd.merge(
                                        pd.merge(
                                            self.mydb.get_dataframe(objct = Project, index = False),
                                            self.mydb.get_dataframe(objct = ProjectType, index = False),
                                            on = 'projecttype_id', how = 'left'
                                                ).drop(
                                                'projecttype_id',
                                                axis=1
                                                      ),
                                        self.mydb.get_dataframe(objct = Customer, index = False).drop(
                                                                                            'address_id',
                                                                                            axis = 1
                                                                                                     ),
                                        on = 'customer_id', how = 'left'
                                            ).drop(
                                            'customer_id',
                                            axis=1
                                                  ),
                                    self.mydb.get_dataframe(objct = Location, index = False).drop(
                                                                                        'legalentity_id',
                                                                                        axis=1
                                                                                                 ),
                                    on = 'location_id', how = 'left'
                                       ).drop(
                                       'location_id',
                                       axis=1
                                             ),
                                ################ E PROJECT DTF ###############
                                on = 'project_id', how = 'left'
                                    ).drop(
                                    'project_id',
                                    axis=1
                                          ),
                            self.mydb.get_dataframe(objct = Location, index = False).drop(
                                                                                'legalentity_id',
                                                                                axis=1
                                                                                         ),
                            on = "location_id", how = 'left'
                                ).drop(
                                "location_id",
                                axis=1
                                      ),
                        # self.mydb.get_dataframe(objct = Center, index = False),
                        # on = 'center_id'
                        #     ).drop(
                        #     'center_id',
                        #     axis=1
                        #           ),
                    ################ E CODE DTF ###############
                    on = 'code_id', how = 'left'
                        ).drop(
                        'code_id',
                        axis=1
                              ),
                self.mydb.get_dataframe(objct = WBSCA, index = False),
                on = 'wbsca_id', how = 'left'
                    ).drop(
                    'wbsca_id',
                    axis=1
                          ).drop(["code_appdate",
                          "code_clodate", "project_clodate",
                          "project_editflag","project_enmodification",
                          "project_appdate","project_rewdate"],
                          axis= 1),
            ############### E WBS DTF ###############
            on = 'wbs_id', how = 'left'
                                    ).drop(
                                    'wbs_id',
                                    axis=1
                                          )
                                      )

        return expenses_dataframe


    def build_GUI(self):
        # L'interface graphique du mdule
        # Elle affiche 3 principaux objets :
        pass
