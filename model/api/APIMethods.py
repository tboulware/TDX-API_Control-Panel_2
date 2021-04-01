import requests
import json
from helpers.LogHelpers import LogHelpers as log
from model.people.Person import Person
from model.api.Group import Group
class APIMethods(object):
    """description of class"""

    __searchMethod = "/people/search"

    @classmethod
    def findPerson(cls, auth, person):
        persons = {}
        if auth.isAuthorized():
            try:
                url = auth.getURLRoot() + cls.__searchMethod
                sess = requests.Session()
                sess.headers = auth.getHeaders()

                search = {}
                search['SearchText'] = person.getLastName()
                search['IsActive'] = True
                resp = sess.post(url, data = json.dumps(search))
       
                persons = json.loads(resp.text)
            except json.JSONDecodeError as jsonex:
                message = f'APIMethods:__findPerson: {str(jsonex.doc)}'
                log.critical(message)
            except Exception as ex:
                message = f'APIMethods:__findPerson: {str(ex)}'
                log.critical(message)
        else:
            message = f'APIMethods: findPerson: not authorized'
            log.warning(message)
     
        return persons

    @classmethod
    def removeGroupMembers(cls, auth, group):
        if auth.isAuthorized():
            try:
                url = auth.getURLRoot() + group.getMethod()
                sess = requests.Session()
                sess.headers = auth.getHeaders()
                resp = sess.get(url)
                currentMembers = json.loads(resp.text)

                uids = []
                if len(currentMembers) > 0:
                    for member in currentMembers:
                        uids.append(member["UID"])
                    delResp = sess.delete(url, data=json.dumps(uids))
            except json.JSONDecodeError as jsonex:
                message = f'APIMethods: __removeCurrentMembers: {str(jsonex.doc)}'
                log.critical(message)
            except Exception as ex:
                message = f'removeGroupMembers: {str(ex)}'
                log.critical(message)
            else:
                message= f'{group.getGroupName()} group has been cleared'
                log.info(message)
                print('________________________________________')
            
        else:
            message = f'APIMethods: removeGroupMembers: not authorized'
            log.warning(message)
            

    @classmethod
    def verifyGroupMember(cls, auth, uids, group):
        if auth.isAuthorized() and len(uids) > 0:
            try:
                url = auth.getURLRoot() + group.getMethod()
                sess = requests.Session()
                sess.headers = auth.getHeaders()
                resp = sess.get(url)

                currentMembers = json.loads(resp.text)
                #get the list of UID
                currentUID = []
                for user in currentMembers:
                    currentUID.append(user['UID'])

                currentUID.sort()
                uids.sort()

                if currentUID == uids:
                    message= f'{group.getGroupName()} group has been verified'
                    log.info(message)
                else:
                    message=f'{groupName} group has NOT been verified'
                    log.warning(message)
            except json.JSONDecodeError as jsonex:
                message = f'APIMethods: verifyGroupMembers: {str(jsonex.doc)}'
                log.critical(message)
            except Exception as ex:
                message= f'APIMethods: verifyGroupMembers: {str(ex)}'
                log.info(message)

        else:
            message = f'APIMethods: verifyGroupMember: not authorized'
            log.warning(message)

    @classmethod
    def addGroupMembers(cls, auth, uids, group):
        valid = False
        if auth.isAuthorized and len(uids) > 0:
            try:
                url = auth.getURLRoot() + group.getMethod()
                sess = requests.Session()
                sess.headers = auth.getHeaders()
                resp = sess.post(url, data=json.dumps(uids))
            except json.JSONDecodeError as jsonex:
                message = f'APIMethods: addGroupMembers: {str(jsonex.doc)}'
                log.critical(message)
            except Exception as ex:
                message = f'APIMethods: addGroupMembers: {str(ex)}'
                log.critical(message)
            else:
                message = f'{len(uids)} members added to {group.getGroupName()}'
                log.info(message)
                valid = True
                print('_______________________________________')
        return valid



