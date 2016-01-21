# Personnal Libs imports
from ressource.object.singleton import Singleton

#This is the User class, has inherited from a metaclass "type"
class User(metaclass=Singleton):

    def __init__(self,login, index):
            self.login = login
            self.index = index
