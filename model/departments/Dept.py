class Dept(object):
    """description of class"""
    
    def __init__(self, code='', name='', acctID ='', isActive =''):
        self.__code = code
        self.__name = name
        self.__ID = acctID
        self.__valid = False
        self.__isActive = True


    def __str__(self):
        value = f'Code: {self.getCode()} Name: {self.getName()}, ID: {self.__ID}, Is Active: {self.__isActive}'
        return value

    def setCode(self, value):
       self.__code = value

    def getCode(self):
        return self.__code

    def setName(self, value):
        self.__name = value

    def getName(self):
        return self.__name

    def setID(self, value):
        self.__ID= value

    def getID(self):
        return self.__ID

    def setValid(self, value):
        self.__valid = value

    def getValid(self):
        return self.__valid

    def setIsActive(self, value):
        self.__isActive = value
        if value == False:
            self.__valid = False

    def getIsActive(self):
        return self.__isActive

