from model.people.PeopleFileOperations import PeopleFileOperations as fileOps
class PersonList(object):
    """Dictionary collection of people"""

    def __init__(self, fileName='peopleList.csv'):
        self.__personList = {}
        self.__filename = fileName
        self.readFile()

    def readFile(self):
        fileOps.openPeopleList(self.__personList, self.__filename)

    def __str__(self):
        str = ""
        for x in self.__personList.values:
            str += str(x) + '\n'

    def add(self, value):
        self.__personList[value.getDuckID()] = value

    def remove(self, value):
        self.__personList.pop(value.getDuckID())

    def find(self, email):
        return self.__personList.get(email)

    def inList(self, primaryEmail):
        return primaryEmail in self.__personList.keys()

    def getList(self):
        return self.__personList

    def isEmpty(self):
        return len(self.__personList) == 0

    def printList(self):
        for key, value in self.__personList.items():
            print(f'{key}:  {value}')



