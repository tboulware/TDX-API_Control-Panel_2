class Group(object):
    """description of class"""

    def __init__(self, method, groupName, fileName):
        self.__method = method
        self.__groupName = groupName
        self.__filename = fileName


    def getMethod(self):
        return self.__method

    def getGroupName(self):
        return self.__groupName

    def getFileName(self):
        return self.__filename