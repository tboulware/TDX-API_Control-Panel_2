class TDXDepartmentList(object):
    """description of class"""

    def __init__(self):
        self.__list = {}

    def __str__(self):
        str = ""
        for x in self.__list.values:
            str += str(c) + '\n'

    def setList(self, theList):
        self.__list = theList

    def add(self, tdxDept):
        self.__list[tdxDept.getCode()] = tdxDept

    def remove(self, tdxDept):
        self.__list.pop(tdxDept.getCode())

    def find(self, tdxDept):
        return self.__list.get(tdxDept.getCode())

    def inList(self, code):
        return code in self.__list.keys()

    def inListByName(self, name):
        inList = False
        for acct in self.__list.values():
            if acct.getName() == name:
                inList = True
                break
        return inList

    def getList(self):
        return self.__list

    def isEmpty(self):
        return len(self.__list == 0)

    def printList(self):
        for key, value in self.__list.items():
            print(value)

    def saveFile(self):
        from departments.DeptFileOperations import DeptFileOperations
        DeptFileOperations.writeFile(self.__list, self.__saveFile)

    def findDeptByName(self, name):
        theAcct = None
        for acct in self.__list.values():
            if acct.getName() == name:
                theAcct = acct
                break
        return theAcct




