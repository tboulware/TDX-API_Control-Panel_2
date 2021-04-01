import time
from model.api.AdminAuth import AdminAuth
from model.people.PersonList import PersonList
from model.people.Person import Person
from helpers.LogHelpers import LogHelpers as log
from model.api.APIMethods import APIMethods
from model.api.Group import Group

class GroupProcessing(object):
    """process the important people list and adds them to group """
   
    def __init__(self, group):
        self.__group = group
        self.__auth = AdminAuth()
        self.__personList = PersonList(self.__group.getFileName())
        
        self.__UID = []
        self.__addedCount = 0
        self.__listCount = 0
        self.__sleep = 1.25

    def processGroupMembers(self):
        self.__removeCurrentMembers()
        self.__findPeople()
        print("Uncomment lines after GUI testing")
        #self.__addMembers()
        #self.__verifyMembers()

    def __findPeople(self):
        if not self.__personList.isEmpty(): 
            try:
                for email in self.__personList.getList():
                    self.__listCount += 1
                    per = self.__personList.find(email)
                    # can only call the find API method 60 times in 60 second, need to pause to slow down the calls
                    time.sleep(self.__sleep)
                    self.__findPersonUID(per)
            except Exception as ex:
                message = f'PeopleOps: __findPeople: {str(ex)}'
                log.critical(message)

    def __addMembers(self):
        valid = False
        if len(self.__UID) > 0:
            valid = APIMethods.addGroupMembers(self.__auth, self.__UID, self.__group)
            if valid:
                if self.__addedCount == self.__listCount:
                    message = f'{self.__addedCount}/{self.__listCount} found: no errors'
                    log.info(message)
                else:
                    diff = self.__listCount-self.__addedCount
                    message = f'{self.__addedCount}/{self.__listCount} found: {diff} errors (not active)'
                    log.warning(message)

            else:
                message=f'Members not added to the group'
                log.critical(message)
        else:
            message = 'People list is empty, no people to process'
            log.warning(message)

    def __findPersonUID(self, person):
        persons = APIMethods.findPerson(self.__auth, person)
        found = False
            
        if len(persons) > 0:
            for per in persons:
                if  person.getEmail() == per["PrimaryEmail"]:
                    person.setUID(per["UID"])
                    person.setAuthUserName(per["AuthenticationUserName"])
                    person.setUserName(per["UserName"])

                    self.__UID.append(per["UID"])
                    self.__addedCount += 1
                    print(f'Count {self.__addedCount}: {person.getDuckID()} ({person.getEmail()} = {per["PrimaryEmail"]})')
                    found = True
                    break;
        if not found:  # add this to the logger 
            message = f'Not found: {str(person)} is not active'
            log.warning(message)

    def __removeCurrentMembers(self):
        APIMethods.removeGroupMembers(self.__auth, self.__group)
            

    def __verifyMembers(self):
         APIMethods.verifyGroupMember(self.__auth,  self.__UID, self.__group)
             