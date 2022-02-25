from helpers.StringHelpers import StringHelpers
class Person(object):
    """Holds the pertinent information for each TDX person record"""

    def __init__(self, duckId='', name='', email=''):
        self.__userName = ''
        self.__authUserName = ''
        self.__name = name
        self.__email = email
        self.__duckID = duckId
        self.__UID = ''

    def __str__(self):
        return f'{self.__name}, duckID: {self.__duckID }, email: {self.__email}'

    def setUserName(self, value):
         self.__userName = value

    def getUserName(self):
        return self.__userName

    def setAuthUserName(self, value):
        self.__authUserName = value

    def getAuthUserName(self):
        return self.__authUserName

    def setFullName(self, value):
         self.__fullName = value

    def getLastName(self):
        return self.__name.split(", ")[0]

    def getFullName(self):
        try:
            names = self.__name.split(", ")
            last = names[0]
            first = names[1].split()[0]
            return first + ' ' + last
        except Exception as ex:
            return self.__name

       

    def setEmail(self, value):
         self.__email = value

    def getEmail(self):
        return  self.__email

    def setDuckID(self, value):
        self.__duckID = value

    def getDuckID(self):
        return self.__duckID

    def getUID(self):
        return self.__UID

    def setUID(self, value):
        self.__UID = value



