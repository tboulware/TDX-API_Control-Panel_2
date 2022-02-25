class GroupInfo(object):
    """description of class"""

    def __init__(self, groupName=None, groupID=None, isActive=None):
        self.__Name = groupName
        self.__ID = groupID
        self.__IsActive = isActive

    def __str__(self):
        return f'{self.__Name}, Id: {self.__ID}, Active: {self.__IsActive}'

    def getName(self):
        return self.__Name

    def setName(self, name):
        self.__Name = name

    def getID(self):
        return self.__ID

    def setID(self, id):
        self.__ID = id

    def setActive(self, active):
        self.__IsActive = active

    def getActive(self):
        return self.__IsActive


        





