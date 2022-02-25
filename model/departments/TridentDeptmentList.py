from model.departments.DeptFileOperations import DeptFileOperations
class TridentDepartmentList(object):
    """Dictionary collection of departments"""

    def __init__(self, fileName):
        self.__list = {}
        self.__fileName = fileName
        self.readFile()

    def readFile(self):
        DeptFileOperations.openDepartmentFile(self.__list, self.__fileName)

    def __str__(self):
        str = ""
        for x in self.__list.values:
            str += str(c) + '\n'

    def add(self, dept):
        self.__list[dept.getCode()] = value

    def remove(self, dept):
        self.__list.pop(dept.getCode())

    def find(self, code):
        return self.__list.get(code)

    def inList(self, code):
        valid = False
        if code in self.__list.keys():
            valid = True
        return valid

    def getList(self):
        return self.__list

    def isEmpty(self):
        return len(self.__list == 0)

    def printList(self):
        for key, value in self.__list.items():
            print(value)

    def findAcctByName(self, name):
        theAcct = None
        for acct in self.__list.values():
            if acct.getName() == name:
                theAcct = acct
                break
        return theAcct








