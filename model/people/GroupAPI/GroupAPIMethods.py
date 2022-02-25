import requests
import json
from helpers.LogHelpers import LogHelpers
from model.people.Person import Person
from model.people.GroupAPI.GroupAPIInfo import GroupAPIInfo
from model.people.GroupInfo import GroupInfo
from model.api.AdminAuth import AdminAuth
class GroupAPIMethods(object):
    """description of class"""

    auth = AdminAuth()

    @classmethod
    def setUseSandBox(cls, useSandbox):
        cls.auth.setUseSandbox(useSandbox)

    searchMethod = "/people/search"
    groupMethod = "/groups/search"

    @classmethod
    def findPerson(cls, person):
        persons = {}
        if cls.auth.isAuthorized():
            try:
                url = cls.auth.getURLRoot() + cls.searchMethod
                sess = requests.Session()
                sess.headers = cls.auth.getHeaders()

                search = {}
                search['SearchText'] = person.getDuckID()
                search['IsActive'] = True
                resp = sess.post(url, data = json.dumps(search))
       
                persons = json.loads(resp.text)
            except json.JSONDecodeError as jsonex:
                message = f'GroupAPIMethods:__findPerson: {str(jsonex.doc)}'
                LogHelpers.critical(message)
            except Exception as ex:
                message = f'GroupAPIMethods:__findPerson: {str(ex)}'
                LogHelpers.critical(message)
        else:
            message = f'GroupAPIMethods: findPerson: not authorized'
            log.warning(message)
     
        return persons

    @classmethod
    def getGroupList(cls):
        groupList = {}
        groupJSONList = []
        if cls.auth.isAuthorized():
            try:
                url = cls.auth.getURLRoot() + cls.groupMethod
                sess = requests.Session()
                sess.headers = cls.auth.getHeaders()
                acctJson = {}
                acctJson['IsActive']='true'
                resp = sess.post(url,  data=json.dumps(acctJson))
                if resp.ok:
                    groupJSONList = json.loads(resp.text)
                    for grp in groupJSONList:
                        name = grp['Name']
                        id = grp['ID']
                        active = grp['IsActive']
                        groupList[id] = GroupInfo(name, id, active)
                else:
                    raise Exception("Group list not returned")
            except json.JSONDecodeError as jsonex:
                message = f'GroupAPIMethods:getGroupList: {str(jsonex.doc)}'
                LogHelpers.critical(message)
            except Exception as ex:
                message = f'GroupAPIMethods:getGroupList:  {str(ex)}'
                LogHelpers.critical(message)
        else:
            message = f'GroupAPIMethods:getGroupList:  not authorized'
            LogHelpers.warning(message)

        return groupList

    @classmethod
    def removeGroupMembers(cls, group):
        if cls.auth.isAuthorized():
            try:
                url = cls.auth.getURLRoot() + "/groups/" + str(group.getID()) + "/members"
                sess = requests.Session()
                sess.headers = cls.auth.getHeaders()
                resp = sess.get(url)
                currentMembers = json.loads(resp.text)

                uids = []
                if len(currentMembers) > 0:
                    for member in currentMembers:
                        uids.append(member["UID"])
                    delResp = sess.delete(url, data=json.dumps(uids))
            except json.JSONDecodeError as jsonex:
                message = f'GroupAPIMethods: removeGroupMembers: {str(jsonex.doc)}'
                LogHelpers.critical(message)
            except Exception as ex:
                message = f'GroupAPIMethods: removeGroupMembers: {str(ex)}'
                LogHelpers.critical(message)
            else:
                message= f'GroupAPIMethods:removeGroupMembers: {group.getName()} group has been cleared'
                LogHelpers.info(message)
        else:
            message = f'GroupAPIMethods: removeGroupMembers: not authorized'
            LogHelpers.warning(message)
            

    @classmethod
    def verifyGroupMember(cls, uids, group):
        if cls.auth.isAuthorized() and len(uids) > 0:
            try:
                url = cls.auth.getURLRoot() + "/groups/" + str(group.getID()) + "/members"
                sess = requests.Session()
                sess.headers = cls.auth.getHeaders()
                resp = sess.get(url)

                currentMembers = json.loads(resp.text)
                #get the list of UID
                currentUID = []
                for user in currentMembers:
                    currentUID.append(user['UID'])

                currentUID.sort()
                uids.sort()

                if currentUID == uids:
                    message= f'GroupAPIMethods:verifyGroupMember: {group.getName()} group has been verified'
                    LogHelpers.info(message)
                else:
                    message=f'GroupAPIMethods:verifyGroupMember: {group.getName()} group has NOT been verified'
                    LogHelpers.warning(message)
            except json.JSONDecodeError as jsonex:
                message = f'GroupAPIMethods:verifyGroupMember: verifyGroupMembers: {str(jsonex.doc)}'
                LogHelpers.critical(message)
            except Exception as ex:
                message= f'GroupAPIMethods:verifyGroupMember: verifyGroupMembers: {str(ex)}'
                LogHelpers.info(message)

        else:
            message = f'GroupAPIMethods: verifyGroupMember: not authorized'
            LogHelpers.warning(message)

    @classmethod
    def addGroupMembers(cls, uids, group):
        valid = False
        if cls.auth.isAuthorized and len(uids) > 0:
            try:
                url = cls.auth.getURLRoot() + "/groups/" + str(group.getID()) + "/members"
                sess = requests.Session()
                sess.headers = cls.auth.getHeaders()
                resp = sess.post(url, data=json.dumps(uids))
            except json.JSONDecodeError as jsonex:
                message = f'GroupAPIMethods:addGroupMembers: addGroupMembers: {str(jsonex.doc)}'
                LogHelpers.critical(message)
            except Exception as ex:
                message = f'GroupAPIMethods:addGroupMembers: addGroupMembers: {str(ex)}'
                LogHelpers.critical(message)
            else:
                message = f'{len(uids)} members added to {group.getName()}'
                LogHelpers.info(message)
                valid = True
        return valid

   