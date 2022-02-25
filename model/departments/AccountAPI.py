import requests
import json
import datetime
import os
from helpers.LogHelpers import LogHelpers
from model.departments.DeptFileOperations import DeptFileOperations
from model.departments.Dept import Dept
from model.api.AdminAuth import AdminAuth

class AccountAPI(object):
    """description of class"""

    __accountEndPoint = "/accounts"
    __tdxArchive = "documenation\\departments"
    auth = AdminAuth()
    useSandbox = True

    @classmethod 
    def setUseSandBox(cls, useSandbox):
        cls.auth.setUseSandbox(useSandbox)

    @classmethod
    def getTDXAccountList(cls):
        theDate = datetime.datetime.now()
        dir = os.getcwd() + "\\" + cls.__tdxArchive + "\\"
        saveFile = dir + "TDXAcctArchive_" + theDate.strftime("%b_%d_%Y_%H_%M") + ".txt"
        tdxAcctJsonList = []
        tdxDeptList = []
        if cls.auth.isAuthorized():
            try:
                url = cls.auth.getURLRoot() + cls.__accountEndPoint 
                sess = requests.Session()
                sess.headers = cls.auth.getHeaders()
                
                resp = sess.get(url)
                if resp.ok:
                    tdxAcctJsonList = json.loads(resp.text)
                    #this is created to store the current TDX Department List for archival
                    tdxDeptList = cls.createObjectList(tdxAcctJsonList)
                    DeptFileOperations.writeFile(tdxDeptList, saveFile)
                else:
                    raise Exception("Account list not returned")
            except json.JSONDecodeError as jsonex:
                message = f'AccountAPI:getTDXAccountList: {str(jsonex.doc)}'
                LogHelpers.critical(message)
            except Exception as ex:
                message = f'AccountAPI:getTDXAccountList: {str(ex)}'
                LogHelpers.critical(message)
        return tdxAcctJsonList

    @classmethod
    def getInactiveList(cls):
        tdxAcctJsonList = []
        tdxDeptList = {}
        if cls.auth.isAuthorized():
            try:
                url = cls.auth.getURLRoot() + cls.__accountEndPoint + '/search'
                sess = requests.Session()
                sess.headers = cls.auth.getHeaders()
                acctJson = {}
                acctJson['IsActive']='false'
                resp = sess.post(url, data=json.dumps(acctJson))
                if resp.ok:
                    tdxAcctJsonList = json.loads(resp.text)
                    for acct in tdxAcctJsonList:
                        code = acct['Code']
                        name = acct['Name']
                        acctID = acct['ID']
                        isActive = acct['IsActive']
                        tdxDeptList[acctID] = Dept(code,name, acctID, isActive)
                else:
                    raise Exception("Account list not returned")
            except json.JSONDecodeError as jsonex:
                message = f'AccountAPI:getInactiveList: {str(jsonex.doc)}'
                LogHelpers.critical(message)
            except Exception as ex:
                message = f'AccountAPI:getInactiveList: {str(ex)}'
                LogHelpers.critical(message)

        return tdxDeptList


    @classmethod
    def createObjectList(cls, tdxAcctJsonList):
        deptList = []
        try:
            for acct in tdxAcctJsonList:
                code = acct['Code']
                name = acct['Name']
                acctID = acct['ID']
                isActive = acct['IsActive']

                dept = Dept(code, name, acctID, isActive)
                deptList.append(dept)
        except Exception as ex:
                message = f'AccountAPI:createObjectList: {str(ex)}'
                LogHelpers.critical(message)

        return deptList

    @classmethod
    def deactivateAccount(cls, acct):
        if cls.auth.isAuthorized():
            try:
                url = cls.auth.getURLRoot() +  cls.__accountEndPoint + '/' + str(acct.getID())
                sess = requests.Session()
                sess.headers = cls.auth.getHeaders()
                acctJson = {}
                acctJson['Name'] = acct.getName()
                acctJson['IsActive']='false'
                resp = sess.put(url, data=json.dumps(acctJson))
                if resp.ok:
                   LogHelpers.info(f'{acct.getName()}, code: {acct.getCode()} deactivated')
                else:
                    raise Exception("Account not deactivated")
            except json.JSONDecodeError as jsonex:
                message = f'AccountAPI:deactivateAccount: {str(jsonex.doc)}'
                LogHelpers.critical(message)
            except Exception as ex:
                message = f'AccountAPI:deactivateAccount: {str(ex)}'
                LogHelpers.critical(message)
        else:
            LogHelpers.critical("deactivateAccount: No Authenicated")
          
    @classmethod
    def activateTDXAccount(cls, acct):
        if cls.auth.isAuthorized():
            try:
                url = cls.auth.getURLRoot() +  cls.__accountEndPoint + '/' + str(acct.getID())
                sess = requests.Session()
                sess.headers = auth.getHeaders()
                acctJson = {}
                acctJson['Name'] = acct.getName()
                acctJson['IsActive']='true'
                acctJson['Code']=acct.getCode()
                resp = sess.put(url, data=json.dumps(acctJson))
                if resp.ok:
                   LogHelpers.info(f'{acct.getName()}, code: {acct.getCode()} activated')
                else:
                    raise Exception("Account not activated")
            except json.JSONDecodeError as jsonex:
                message = f'AccountAPI:activateTDXAccount: {str(jsonex.doc)}'
                LogHelpers.critical(message)
            except Exception as ex:
                message = f'AccountAPI:activateTDXAccount: {str(ex)}'
                LogHelpers.critical(message)
        else:
            log.critical("activateTDXAccount: No Authenicated")

    @classmethod
    def setTDXName(cls, acct, correctName):
        success = False
        if cls.auth.isAuthorized():
            try:
                url = cls.auth.getURLRoot() +  cls.__accountEndPoint + '/' + str(acct.getID())
                sess = requests.Session()
                sess.headers = cls.auth.getHeaders()
                acctJson = {}
                acctJson['Name'] = correctName
                acctJson['IsActive']='true'
                resp = sess.put(url, data=json.dumps(acctJson))
                if resp.status_code == 201:
                    log.info(f'TDX Account name change {acct.getCode()}, Name: {acct.getName()} --> {correctName}')
                    success = True
                else:
                    raise Exception(f'Response code: {resp.status_code} {acct.getName()} name not changed')
            except json.JSONDecodeError as jsonex:
                message = f'AccountAPI:setTDXName: {str(jsonex.doc)}'
                LogHelpers.critical(message)
            except Exception as ex:
                message = f'AccountAPI:setTDXName: {str(ex)}'
                LogHelpers.critical(message)
            else:
                print(f'{acct.getName()}, code: {acct.getCode()} name changed')

        return success

    @classmethod
    def setTDXAccountCode(cls, acct):
        success = False
        if cls.auth.isAuthorized():
            try:
                url = cls.auth.getURLRoot() +  cls.__accountEndPoint + '/' + str(acct.getID())
                sess = requests.Session()
                sess.headers = cls.auth.getHeaders()
                acctJson = {}
                acctJson['Name'] = acct.getName()
                acctJson['Code']= acct.getCode()
                resp = sess.put(url, data=json.dumps(acctJson))
                if resp.status_code == 201:
                    log.info(f'TDX Account code change {acct.getCode()}: Name: {acct.getName()}')
                    success = True
                else:
                    raise Exception(f'Response code: {resp.status_code} {acct.getName()} name not changed')
            except json.JSONDecodeError as jsonex:
                message = f'AccountAPI:setTDXName: {str(jsonex.doc)}'
                LogHelpers.critical(message)
            except Exception as ex:
                message = f'AccountAPI:setTDXName: {str(ex)}'
                LogHelpers.critical(message)
            else:
                print(f'{acct.getName()}, code: {acct.getCode()} name changed')

        return success

    @classmethod
    def createTDXAccount(cls, acct):
        success = False
        if cls.auth.isAuthorized():
            try:
                url = cls.auth.getURLRoot() +  cls.__accountEndPoint 
                sess = requests.Session()
                sess.headers = cls.auth.getHeaders()
                acctJson = {}
                acctJson['Name'] = acct.getName()
                acctJson['Code']= acct.getCode()
                resp = sess.post(url, data=json.dumps(acctJson))
                if resp.ok:
                    log.info(f'TDX Account added: {acct.getCode()}: Name: {acct.getName()}')
                    success = True
                else:
                    raise Exception(f'Response code: {resp.status_code} {acct.getName()} not added')
            except json.JSONDecodeError as jsonex:
                message = f'AccountAPI:createTDXAccount: {str(jsonex.doc)}'
                LogHelpers.critical(message)
            except Exception as ex:
                message = f'AccountAPI:createTDXAccount: {str(ex)}'
                LogHelpers.critical(message)

        return success





