class Address(object):
    """location address"""

    def __init__(self, street='', city='Eugene', state='OR', zip='97403'):
        self.__street = street
        self.__city = city
        self.__state = state
        self.__zip = zip

    def __eq__(self, other):
       return self.__street.strip().lower() == other.__street.strip().lower()

    def __str__(self):
        return self.__street + " " + self.__city + ", " + self.__state

    def setStreet(self, value):
        self.__street = value

    def getStreet(self):
        return self.__street

    def setCity(self, value):
        self.__city = value

    def getCity(self):
        return self.__city

    def setState(self, value):
        self.__state = value

    def getState(self):
        return self.__state

    def setZip(self, value):
        self.__zip = value

    def getZip(self):
        return self.__zip


