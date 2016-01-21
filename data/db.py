#Python Libs imports
import pandas as pd

#Personnal Libs imports
from ressource.object.singleton import Singleton

#Class of the dtb
class MyDB(metaclass=Singleton):

    # We define the path to the local dtb
    local_path = "D:\\Programmation\\Mascaret\\Programme Mascaret 2.0\\data\\localtables\\"

#-------------------------------------------------------------------------------

    # def get_dataframe(self, objct, index = True, mode='local'):
    # # This methode get a DataFrame of the objet we want
    #     # Mode Local
    #     if mode == 'local':
    #         if index == True:
    #             return pd.read_csv( self.local_path + objct._dtb_table,
    #                 names = objct._dtb_columns, index_col = 0)
    #         else:
    #             return pd.read_csv( self.local_path + objct._dtb_table,
    #                 names = objct._dtb_columns)



    def get_dataframe(self, objct, index = True, mode='local'):
    # This methode gets a DataFrame of the objet we want
        # Mode Local
        if mode != 'local':
            return
        index_column = 0 if index == True else None
        return pd.read_csv( self.local_path + objct._dtb_table, names =
        objct._dtb_columns, index_col = index_column)



# Archives

#
# #Class of the dtb
# class MyDB(metaclass=Singleton):
#
#     def __init__(self):
#         self._db_connection = pymysql.connect(
#                                             'localhost',
#                                             'root',
#                                             '',
#                                             'mascaretdb'
#                                              )
#         self._db_cur = self._db_connection.cursor()
#         self._db_connection.autocommit(False)
#         self.a_listAddresses = []
#         self.a_listCenters = []
#         self.a_listClassifications = []
#         self.a_listCodeTypes = []
#         self.a_listCostElements = []
#         self.a_listCustomers = []
#         self.a_listEmployees = []
#         self.a_listLegalEntities = []
#         self.a_listExpenses = []
#         self.a_listFunctions = []
#         self.a_listGroupCostElement = []
#         self.a_listLocations = []
#         self.a_listModules = []
#         self.a_listProjects = []
#         self.a_listProjectTypes = []
#         self.a_listRoles = []
#         self.a_listServices = []
#         self.a_listStatus = []
#         self.a_listTools = []
#         self.a_listToolTypes = []
#         self.a_listCenterExpensesTypes = []
#         self.a_listUsers = []
#         self.a_listwbsCA = []
#         self.a_listWBSElements = []
#         print("initialisation de la db")
#
#     def query(self, query, params):
#         self._db_cur.execute(query, params)
#
#     def db_fetchall(self):
#         return self._db_cur.fetchall()
#
#     def __del__(self):
#         self._db_connection.close()
#         print("Destruction de la db")
#
#     def commit(self):
#         self._db_connection.commit()
#
#     def rollback(self):
#         self._db_connection.rollback()
#
# #-------------------------------------------------------------------------------
#     def addAddress(self, i_address):
#         if self.getAddress(i_address.a_index):
#             return false
#         self.a_listAddresses.append(i_address)
#         return true
#
#     def removeAddress(self, i_address):
#         if i_address not in a_listAddresses:
#             return false
#         self.a_listAddresses.remove(i_address)
#         return true
#
#     def getExistantAddress(self, i_index):
#         for address in self.a_listAddresses:
#             if address.a_index == i_index:
#                 return address
#             else:
#                 return none
#
# #-------------------------------------------------------------------------------
#     def addCenter(self, i_center):
#         if self.getCenter(i_center.a_index):
#             return false
#         self.a_listCenters.append(i_center)
#         return true
#
#     def removeCenter(self, i_center):
#         if i_center not in a_listCenters:
#             return false
#         self.a_listCenters.remove(i_center)
#         return true
#
#     def getExistantCenter(self, i_index):
#         for center in self.a_listCenters:
#             if center.a_index == i_index:
#                 return center
#             else:
#                 return none
#
# #-------------------------------------------------------------------------------
#     def addClassification(self, i_classification):
#         if self.getClassification(i_classification.a_index):
#             return false
#         self.a_listClassifications.append(i_classification)
#         return true
#
#     def removeClassification(self, i_classification):
#         if i_classification not in a_listClassifications:
#             return false
#         self.a_listClassifications.remove(i_classification)
#         return true
#
#     def getExistantClassification(self, i_index):
#         for classification in self.a_listClassifications:
#             if classification.a_index == i_index:
#                 return classification
#             else:
#                 return none
#
# #-------------------------------------------------------------------------------
#     def addCodeType(self, i_type):
#         if self.getCodeType(i_type.a_index):
#             return false
#         self.a_listCodeTypes.append(i_type)
#         return true
#
#     def removeCodeType(self, i_type):
#         if i_type not in a_listCodeTypes:
#             return false
#         self.a_listCodeTypes.remove(i_type)
#         return true
#
#     def getExistantCodeType(self, i_index):
#         for codType in self.a_listCodeTypes:
#             if codType.a_index == i_index:
#                 return codType
#             else:
#                 return none
#
# #-------------------------------------------------------------------------------
#     def addCostElement(self, i_element):
#         if self.getCostElement(i_element.a_index):
#             return false
#         self.a_listCostElements.append(i_element)
#         return true
#
#     def removeCostElement(self, i_element):
#         if i_service not in a_listCostElements:
#             return false
#         self.a_listCostElements.remove(i_element)
#         return true
#
#     def getExistantCostElement(self, i_index):
#         for element in self.a_listCostElements:
#             if element.a_index == i_index:
#                 return element
#             else:
#                 return none
#
# #-------------------------------------------------------------------------------
#     def addCustomer(self, i_customer):
#         if self.getCustomer(i_customer.a_index):
#             return false
#         self.a_listCustomers.append(i_customer)
#         return true
#
#     def removeCustomer(self, i_customer):
#         if i_customer not in a_listCustomers:
#             return false
#         self.a_listCustomers.remove(i_customer)
#         return true
#
#     def getExistantCustomer(self, i_index):
#         for customer in self.a_listCustomers:
#             if customer.a_index == i_index:
#                 return customer
#             else:
#                 return none
#
# #-------------------------------------------------------------------------------
#     def addEmployee(self, i_employee):
#         if self.getEmployee(i_employee.a_index):
#             return false
#         self.a_listEmployees.append(i_employee)
#         return true
#
#     def removeEmployee(self, i_employee):
#         if i_employee not in a_listEmployees:
#             return false
#         self.a_listEmployees.remove(i_employee)
#         return true
#
#     def getExistantEmployee(self, i_index):
#         for employee in self.a_listEmployees:
#             if employee.a_index == i_index:
#                 return employee
#             else:
#                 return none
#
# #-------------------------------------------------------------------------------
#     def addLegalEntity(self, i_entity):
#         if self.getLegalEntity(i_entity.a_index):
#             return false
#         self.a_listLegalEntities.append(i_entity)
#         return true
#
#     def removeLegalEntity(self, i_entity):
#         if i_entity not in a_listLegalEntities:
#             return false
#         self.a_listLegalEntities.remove(i_entity)
#         return true
#
#     def getExistantLegalEntity(self, i_index):
#         for entity in self.a_listLegalEntities:
#             if entity.a_index == i_index:
#                 return entity
#             else:
#                 return none
#
# #-------------------------------------------------------------------------------
#     def addExpense(self, i_expense):
#         if self.getExpense(i_expense.a_index):
#             return false
#         self.a_listExpenses.append(i_expense)
#         return true
#
#     def removeExpense(self, i_expense):
#         if i_expense not in a_listExpenses:
#             return false
#         self.a_listExpenses.remove(i_expense)
#         return true
#
#     def getExistantExpense(self, i_index):
#         for expense in self.a_listExpenses:
#             if expense.a_index == i_index:
#                 return expense
#             else:
#                 return none
#
# #-------------------------------------------------------------------------------
#     def addFunction(self, i_function):
#         if self.getFunction(i_function.a_index):
#             return false
#         self.a_listFunctions.append(i_function)
#         return true
#
#     def removeFunction(self, i_function):
#         if i_function not in a_listFunctions:
#             return false
#         self.a_listFunctions.remove(i_function)
#         return true
#
#     def getExistantFunction(self, i_index):
#         for function in self.a_listFunctions:
#             if function.a_index == i_index:
#                 return function
#             else:
#                 return none
#
# #-------------------------------------------------------------------------------
#     def addGroupCostElement(self, i_group):
#         if self.getGroupCostElement(i_group.a_index):
#             return false
#         self.a_listGroupCostElement.append(i_group)
#         return true
#
#     def removeGroupCostElement(self, i_group):
#         if i_group not in a_listGroupCostElement:
#             return false
#         self.a_listGroupCostElement.remove(i_group)
#         return true
#
#     def getExistantGroupCostElement(self, i_index):
#         for group in self.a_listGroupCostElement:
#             if group.a_index == i_index:
#                 return group
#             else:
#                 return none
#
# #-------------------------------------------------------------------------------
#     def addLocation(self, i_location):
#         if self.getLocation(i_location.a_index):
#             return false
#         self.a_listLocation.append(i_location)
#         return true
#
#     def removeLocation(self, i_location):
#         if i_location not in a_listLocation:
#             return false
#         self.a_listLocation.remove(i_location)
#         return true
#
#     def getExistantLocation(self, i_index):
#         for location in self.a_listLocation:
#             if location.a_index == i_index:
#                 return location
#             else:
#                 return none
#
# #-------------------------------------------------------------------------------
#     def addModule(self, i_module):
#         if self.getModule(i_module.a_index):
#             return false
#         self.a_listModules.append(i_module)
#         return true
#
#     def removeModule(self, i_module):
#         if i_module not in a_listModules:
#             return false
#         self.a_listModules.remove(i_module)
#         return true
#
#     def getExistantModule(self, i_index):
#         for module in self.a_listModules:
#             if module.a_index == i_index:
#                 return module
#             else:
#                 return none
#
# #-------------------------------------------------------------------------------
#     def addProject(self, i_project):
#         if self.getProject(i_project.a_index):
#             return false
#         self.a_listProjects.append(i_project)
#         return true
#
#     def removeProject(self, i_project):
#         if i_project not in a_listProjects:
#             return false
#         self.a_listProjects.remove(i_project)
#         return true
#
#     def getExistantProject(self, i_index):
#         for project in self.a_listProjects:
#             if project.a_index == i_index:
#                 return project
#             else:
#                 return none
#
# #-------------------------------------------------------------------------------
#     def addProjectType(self, i_type):
#         if self.getProjectType(i_type.a_index):
#             return false
#         self.a_listProjectTypes.append(i_type)
#         return true
#
#     def removeProjectType(self, i_type):
#         if i_type not in a_listProjectTypes:
#             return false
#         self.a_listProjectTypes.remove(i_type)
#         return true
#
#     def getExistantProjectType(self, i_index):
#         for projectType in self.a_listProjectTypes:
#             if projectType.a_index == i_index:
#                 return projectType
#             else:
#                 return none
#
# #-------------------------------------------------------------------------------
#     def addRole(self, i_role):
#         if self.getRole(i_role.a_index):
#             return false
#         self.a_listRoles.append(i_role)
#         return true
#
#     def removeRole(self, i_role):
#         if i_role not in a_listRoles:
#             return false
#         self.a_listRoles.remove(i_role)
#         return true
#
#     def getExistantRole(self, i_index):
#         for role in self.a_listRoles:
#             if role.a_index == i_index:
#                 return role
#             else:
#                 return none
#
# #-------------------------------------------------------------------------------
#     def addService(self, i_service):
#         if self.getService(i_service.a_index):
#             return false
#         self.a_listServices.append(i_service)
#         return true
#
#     def removeService(self, i_service):
#         if i_service not in a_listServices:
#             return false
#         self.a_listServices.remove(i_service)
#         return true
#
#     def getExistantService(self, i_index):
#         for service in self.a_listServices:
#             if service.a_index == i_index:
#                 return service
#             else:
#                 return none
#
# #-------------------------------------------------------------------------------
#     def addStatus(self, i_status):
#         if self.getStatus(i_status.a_index):
#             return false
#         self.a_listStatus.append(i_status)
#         return true
#
#     def removeStatus(self, i_status):
#         if i_status not in a_listStatus:
#             return false
#         self.a_listStatus.remove(i_status)
#         return true
#
#     def getExistantStatus(self, i_index):
#         for status in self.a_listStatus:
#             if status.a_index == i_index:
#                 return status
#             else:
#                 return none
#
# #-------------------------------------------------------------------------------
#     def addTool(self, i_tool):
#         if self.getTool(i_tool.a_index):
#             return false
#         self.a_listTools.append(i_tool)
#         return true
#
#     def removeTool(self, i_tool):
#         if i_tool not in a_listTools:
#             return false
#         self.a_listTools.remove(i_tool)
#         return true
#
#     def getExistantTool(self, i_index):
#         for tool in self.a_listTools:
#             if tool.a_index == i_index:
#                 return tool
#             else:
#                 return none
#
# #-------------------------------------------------------------------------------
#     def addToolType(self, i_toolType):
#         if self.getToolType(i_toolType.a_index):
#             return false
#         self.a_listToolTypes.append(i_toolType)
#         return true
#
#     def removeToolType(self, i_toolType):
#         if i_toolType not in a_listToolTypes:
#             return false
#         self.a_listToolTypes.remove(i_toolType)
#         return true
#
#     def getExistantToolType(self, i_index):
#         for toolType in self.a_listToolTypes:
#             if toolType.a_index == i_index:
#                 return toolType
#             else:
#                 return none
#
# #-------------------------------------------------------------------------------
#     def addCenterExpensesType(self, i_type):
#         if self.getCenterExpensesType(i_type.a_index):
#             return false
#         self.a_listCenterExpensesTypes.append(i_type)
#         return true
#
#     def removeCenterExpensesType(self, i_type):
#         if i_type not in a_listCenterExpensesTypes:
#             return false
#         self.a_listCenterExpensesTypes.remove(i_type)
#         return true
#
#     def getExistantCenterExpensesType(self, i_index):
#         for center in self.a_listCenterExpensesTypes:
#             if center.a_index == i_index:
#                 return center
#             else:
#                 return none
#
# #-------------------------------------------------------------------------------
#     def addUser(self, i_user):
#         if self.getUser(i_user.a_index):
#             return false
#         self.a_listUsers.append(i_user)
#         return true
#
#     def removeUser(self, i_user):
#         if i_user not in a_listUsers:
#             return false
#         self.a_listUsers.remove(i_ca)
#         return true
#
#     def getExistantUser(self, i_index):
#         for user in self.a_listUsers:
#             if user.a_index == i_index:
#                 return user
#             else:
#                 return none
#
# #-------------------------------------------------------------------------------
#     def addWBSCa(self, i_ca):
#         if self.getWBSCa(i_ca.a_index):
#             return false
#         self.a_listwbsCA.append(i_ca)
#         return true
#
#     def removeWBSCa(self, i_ca):
#         if i_ca not in a_listwbsCA:
#             return false
#         self.a_listwbsCA.remove(i_ca)
#         return true
#
#     def getExistantWBSCa(self, i_index):
#         for ca in self.a_listwbsCA:
#             if ca.a_index == i_index:
#                 return ca
#             else:
#                 return none
#
# #-------------------------------------------------------------------------------
#     def addWBSElement(self, i_element):
#         if self.getWBSElement(i_element.a_index):
#             return false
#         self.a_listWBSElements.append(i_element)
#         return true
#
#     def removeWBSElement(self, i_element):
#         if i_element not in a_listWBSElements:
#             return false
#         self.a_listWBSElements.remove(i_element)
#         return true
#
#     def getExistantWBSElement(self, i_index):
#         for element in self.a_listWBSElements:
#             if element.a_index == i_index:
#                 return element
#             else:
#                 return none
#
# #-------------------------------------------------------------------------------
#     #Methode caca de Julien
#     def get_all_ent_jur(self):
#         get_all_legal_entities_query = "SELECT *FROM EntiteJuridique;"
#         try:
#             self.query(get_all_legal_entities_query,[])
#             self.commit()
#         except:
#             self.rollback()
#         #On obtient une matrice
#         legal_entities_data = self.db_fetchall()
#         # Liste d'entite Juridique
#         data_ent_jur = ListLegalEntity(legal_entities_data)
#
#         return data_ent_jur
#
#     #Methode caca de Julien
#     def check_existence_of_new_ent_jur_and_add_it_db(
#                                                     self,data_ent_jur,
#                                                     entity_text
#                                                     ):
#         entity_exist = False
#         for row in data_ent_jur:
#             if (row.intitule == entity_text):
#                 print("This Legal Entity already exists")
#                 entity_exist = True
#         if entity_exist == False:
#             add_legal_entity_query = (
#                 "INSERT INTO `entitejuridique` (`intitule`) VALUES (%s) ;"
#                                      )
#
#             parameters_query = [str(entity_text)]
#
#             try:
#                 self.query(add_legal_entity_query,parameters_query)
#                 self.commit()
#             except:
#                 self.rollback()
#         return entity_exist
#
#     def get_location_list_db(self):
#         get_all_location_query = "SELECT * FROM Location;"
#
#         try:
#             self.query(get_all_location_query,[])
#
#             self.commit()
#         except:
#             self.rollback()
#         #On obtient une matrice
#         location_data = self.db_fetchall()
#         # Liste d'entite Juridique
#         data_location = ListLocationFromFetch(location_data)
#
#         return data_location
#
#     def check_existence_of_new_location_and_add_it_db(
#                                                     self,data_location,
#                                                     location_text,location_id
#                                                      ):
#
#         location_exist = False
#         for row in data_location:
#             if row.intitule == location_text:
#                 print("This Location already exists")
#                 location_exist = True
#
#         if location_exist == False:
#             try:
#                 idEntJur= location_id
#
#                 add_permission_query = (
#                 "INSERT INTO `permission` (`idPermission`) VALUES (NULL) ;"
#                                        )
#                 self.query(add_permission_query,[])
#
#                 get_idpermission_query = (
#                         """SELECT P.idPermission AS Id FROM permission P
#                         ORDER BY P.idPermission DESC LIMIT 1;"""
#                                          )
#                 self.query(get_idpermission_query,[])
#                 get_permission_id_data = self.db_fetchall()
#
#                 add_location_query = (
#                     """INSERT INTO `location` (idLoc, intitule, idEntJur)
#                     VALUES (%s,%s,%s);"""
#                                      )
#
#                 parameters_query = [
#                                 get_permission_id_data,
#                                 location_text,idEntJur
#                                    ]
#                 self.query(add_location_query,parameters_query)
#                 self.commit()
#             except:
#                 self.rollback()
#
#         return location_exist
#
# #----------------------------------------------------------------------------------------------
#     def get_service_list_db(self):
#         get_all_service_query = "SELECT * FROM Service;"
#         try:
#             self.query(get_all_service_query,[])
#
#             self.commit()
#         except:
#             self.rollback()
#         #On obtient une matrice
#         service_data = self.db_fetchall()
#         # Liste de service
#         data_service = ListServiceFromFetch(service_data)
#         return data_service
#
# #----------------------------------------------------------------------------------------------
#     def fetchCenter(self, i_idCenter):
#         get_center_query = "SELECT * FROM Center WHERE Center.idCenter = %s;"
#         parameters_query = [i_idCenter]
#         try:
#             self.query(get_center_query,parameters_query)
#
#             self.commit()
#         except:
#             self.rollback()
#         #On obtient une matrice
#         center_data = self.db_fetchall()
#         # Liste de service
#         data_center = ListCenterFromFetch(center_data)
#         return data_center
#
#     def getCenter(self, i_idCenter):
#         center = self.getCenter(i_idCenter)
#         if center:
#             return center
#         fetch = self.fetchCenter(i_idCenter)
#         service = self.getService(fetch[2])
#         newCenter = Center(fetch[0],fetch[1],fetch[3],service)
#         self.addCenter(newCenter)
#         return newCenter
#
# #----------------------------------------------------------------------------------------------
#     def fetchService(self, i_idService):
#         get_service_query = (
#                     "SELECT * FROM Service WHERE Service.idService = %s;"
#                             )
#         parameters_query = [i_idService]
#         try:
#             self.query(get_service_query,parameters_query)
#
#             self.commit()
#         except:
#             self.rollback()
#         #On obtient une matrice
#         service_data = self.db_fetchall()
#         # Liste de service
#         data_service = ListServiceFromFetch(service_data)
#         return data_service
#
#     def getService(self, i_idService):
#         service = self.getService(i_idService)
#         if service:
#             return service
#         fetch = self.fetchService(i_idService)
#         location = self.getLocation(fetch[1])
#         newService = Location(fetch[0],fetch[2],location)
#         self.addService(newService)
#         return newService
#
# #----------------------------------------------------------------------------------------------
#     def fetchLocation(self, i_idLocation):
#         get_location_query = (
#             "SELECT * FROM Location WHERE Location.idLocation = %s;"
#                              )
#         parameters_query = [i_idlocation]
#         try:
#             self.query(get_location_query,parameters_query)
#
#             self.commit()
#         except:
#             self.rollback()
#         #On obtient une matrice
#         location_data = self.db_fetchall()
#         # Liste de location
#         data_location = ListLocationFromFetch(location_data)
#         return data_location
#
#     def getLocation(self, i_idLocation):
#         location = self.getExistantLocation(i_idLocation)
#         if location:
#             return location
#         fetch = self.fetchLocation(i_idLocation)
#         legentity = self.getLegalEntity(fetch[2])
#         newLocation = Location(fetch[0],fetch[1],legentity)
#         self.addLocation(newLocation)
#         return newLocation
#
# #----------------------------------------------------------------------------------------------
#     def fetchLegalEntity(self, i_idLegalEntity):
#         get_legalentity_query = (
#         "SELECT * FROM LegalEntity WHERE LegalEntity.idLegalEntity = %s;"
#                                 )
#         parameters_query = [i_idLegalEntity]
#         try:
#             self.query(get_legalentity_query,parameters_query)
#             self.commit()
#         except:
#             self.rollback()
#         #On obtient une matrice
#         legalentity_data = self.db_fetchall()
#         # Creation legalentity
#         legEntity = CreateLegalEntityFromFetch(legalentity_data)
#         return legEntity
#
#
#     def getLegalEntity(self, i_idLegalEntity):
#         entity = self.getExistantLegalEntity(i_idLegalEntity)
#         if entity:
#             return entity
#         fetch = self.fetchLegalEntity(i_idLegalEntity)
#         newLegalEntity = LegalEntity(int(fetch[0]),str(fetch[1]))
#         self.addLegalEntity(newLegalEntity)
#         return newLegalEntity
#
#
# #----------------------------------------------------------------------------------------------
#     def check_existence_of_new_service_and_add_it_db(
#                                                     self,data_service,
#                                                     service_text,location_id
#                                                     ):
#
#         service_exist = False
#         for row in data_service:
#             if row.intitule == service_text:
#                 print("This service already exists")
#                 service_exist = True
#
#         if service_exist == False:
#
#             try:
#                 idLocation= location_id
#
#                 add_permission_query = (
#                 "INSERT INTO `permission` (`idPermission`) VALUES (NULL) ;"
#                                        )
#                 self.query(add_permission_query,[])
#
#                 get_idpermission_query = (
#                         """SELECT P.idPermission AS Id FROM permission P
#                         ORDER BY P.idPermission DESC LIMIT 1;"""
#                                          )
#                 self.query(get_idpermission_query,[])
#                 get_permission_id_data = self.db_fetchall()
#
#                 add_service_query = (
#                     """INSERT INTO `service` (idservice, intitule, idLocation)
#                     VALUES (%s,%s,%s);"""
#                                     )
#
#                 parameters_query = [
#                                 get_permission_id_data,
#                                 service_text,idLocation
#                                    ]
#                 self.query(add_service_query,parameters_query)
#                 self.commit()
#             except:
#                 self.rollback()
#
#         return service_exist
