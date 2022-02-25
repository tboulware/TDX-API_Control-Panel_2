import time
from model.api.AdminAuth import AdminAuth
from model.people.PersonList import PersonList
from model.people.Person import Person
from helpers.LogHelpers import LogHelpers
from model.people.GroupAPI.GroupAPIMethods import GroupAPIMethods
from model.people.GroupAPI.GroupAPIMethods import GroupAPIInfo

class GroupProcessing(object):
    """process the important people list and adds them to group """
   
    def __init__(self, group, fileName, useSandBox):
        self.__group = group
        self.__personList = PersonList(fileName)
        self.__useSandbox = useSandBox
        GroupAPIMethods.setUseSandBox(self.__useSandbox)
        
        self.__UID = []
        self.__addedCount = 0
        self.__listCount = 0
        self.__sleep = 1.05

    def processGroupMembers(self):
        self.__removeCurrentMembers()
        self.__findPeople()
        self.__addMembers()
        self.__verifyMembers()

    def __findPeople(self):
        count = 0
        if not self.__personList.isEmpty(): 
            try:
                for email in self.__personList.getList():
                    self.__listCount += 1
                    count += 1
                    per = self.__personList.find(email)
                    # can only call the find API method 60 times in 60 second, need to pause to slow down the calls
                    print(f'{self.__listCount}')
                    time.sleep(self.__sleep)
                    self.__findPersonUID(per)
            except Exception as ex:
                message = f'PeopleOps: __findPeople: {str(ex)}'
                LogHelpers.critical(message)

    def __addMembers(self):
        valid = False
        message = f'Adding members: {self.__group.getName()}'
        LogHelpers.displayHeader(message)
        if len(self.__UID) > 0:
            valid = GroupAPIMethods.addGroupMembers(self.__UID, self.__group)
            if valid:
                if self.__addedCount == self.__listCount:
                    message = f'{self.__addedCount}/{self.__listCount} found: no errors'
                    LogHelpers.info(message)
                else:
                    diff = self.__listCount-self.__addedCount
                    message = f'{self.__addedCount}/{self.__listCount} found: {diff} errors (not active)'
                    LogHelpers.warning(message)

            else:
                message=f'Members not added to the group'
                LogHelpers.critical(message)
        else:
            message = 'People list is empty, no people to process'
            LogHelpers.warning(message)
        LogHelpers.displaySeparator()

    def __findPersonUID(self, person):
        persons = GroupAPIMethods.findPerson(person)
        found = False
            
        if len(persons) > 0:
            for per in persons:
                if  person.getEmail() == per["PrimaryEmail"]:
                    person.setUID(per["UID"])
                    person.setAuthUserName(per["AuthenticationUserName"])
                    person.setUserName(per["UserName"])

                    self.__UID.append(per["UID"])
                    self.__addedCount += 1
                    LogHelpers.debug(f'Count {self.__addedCount}: {person.getDuckID()} ({person.getEmail()} = {per["PrimaryEmail"]})')
                    found = True
                    break
        if not found:  # add this to the logger 
            message = f'Not found: {str(person)} is not active'
            LogHelpers.warning(message)

    def __removeCurrentMembers(self):
        message = f'Removing current members: {self.__group.getName()}'
        LogHelpers.displayHeader(message)
        GroupAPIMethods.removeGroupMembers(self.__group)
        LogHelpers.displaySeparator()
            

    def __verifyMembers(self):
         message = f'Verifying group members: {self.__group.getName()}'
         LogHelpers.displayHeader(message)
         GroupAPIMethods.verifyGroupMember(self.__UID, self.__group)
         LogHelpers.displaySeparator()
             