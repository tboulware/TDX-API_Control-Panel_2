import time
from helpers.LogHelpers import LogHelpers 
from model.api.AdminAuth import AdminAuth
from model.departments.TridentDeptmentList import TridentDepartmentList
from model.departments.TDXDepartmentList import TDXDepartmentList

from model.departments.Dept import Dept
from model.departments.AccountAPI import AccountAPI

class DepartmentProcessing(object):
    """description of class"""
    
    def __init__(self, fileName, useSandBox):
        self.__fileName = fileName
        self.__useSandbox = useSandBox

        AccountAPI.setUseSandBox(self.__useSandbox)
        self.__TridentDeptList = TridentDepartmentList(fileName) #retrieves Trident list from CSV file as part of the constructor
        self.__TDXDepart = TDXDepartmentList()
        self.__BadTDXList = TDXDepartmentList()
        self.__InactiveTDXList = TDXDepartmentList()
        self.__NoCodeList = {}
        self.__sleep = 1.05
        self.__acctExceptions = { 'AUTH-ONLY': 'AUTH-ONLY', 
                                 'Public': 'Public',
                                 'Students': 'Students',
                                 'University of Oregon': 'University of Oregon'}
        
    def processDeparments(self):
        self.__processedCount = 0

        try:
            self.getTDXAccountList()
            self.deactivateInvalidTDXAccounts()
            self.validateTDXAccountNames()
            self.setEmptyCodeAccts()
            self.createNewDepartments()
        except Exception as ex:
            print(ex)

    def createNewDepartments(self):
        count = 0
        tridentAcctList = self.__TridentDeptList.getList()
        try:
            #inspects the Trident account list and creates any accounts
            #not found in the TDX Account List.  If the name/code is not found
            #in the TDX Account List, create a new account
            self.__InactiveTDXList.setList(AccountAPI.getInactiveList())
            for code in tridentAcctList:
                tridentAccount = tridentAcctList[code]
                tdxAccount = self.__TDXDepart.find(tridentAccount)
                if tdxAccount is None:
                    tdxAccount = self.__InactiveTDXList.findDeptByName(tridentAccount.getName())
                    if not tdxAccount is None:
                        tdxAccount.setCode(tridentAccount.getCode())
                        AccountAPI.activateTDXAccount(tdxAccount)
                        count += 1
                    #double check if the name is in the list, to prevent 
                    #code/name inconsistencies in TDX
                    elif not self.__TDXDepart.inListByName(tridentAccount.getName()):
                        AccountAPI.createTDXAccount(tridentAccount, self.__auth)
                        count += 1

        except Exception as ex:
            LogHelpers.critical(f'DepartmentProcessing: createNewDepartments {str(ex)}')

        LogHelpers.info(f'{count} new TDX departments created/activated')

    def setEmptyCodeAccts(self):
        try:
            for key in self.__NoCodeList:
                acct = self.__NoCodeList[key]
                tridentAcct = self.__TridentDeptList.findAcctByName(acct.getName())
                if not (tridentAcct is None):
                    acct.setCode(tridentAcct.getCode())
                    AccountAPI.setTDXAccountCode(acct)
                self.__processedCount += 1
        except Exception as ex:
            LogHelpers.critical(f'DepartmentProcessing: setEmptyCodeAccts {str(ex)}')
       
    def validateTDXAccountNames(self):
        #looks at the active list of valid TDXAccounts and compares the TDX Dept name
        #to the Trident department name, if the Trident names does not match
        #the TDX Dept name, then change the TDX Dept name to the Trident Name
        count = 0
        success = False
        tdxAcctList = self.__TDXDepart.getList()
        LogHelpers.displayHeader("Validate TDX Acct Names")
    
        try:
            for acct in tdxAcctList.values():
                if not acct.getName() in self.__acctExceptions.keys():
                    tridentDept =  self.__TridentDeptList.find(acct.getCode())
                    if not (tridentDept.getName() == acct.getName()):
                        success = AccountAPI.setTDXName(acct, tridentDept.getName())
                        if success:
                            count += 1
                        time.sleep(self.__sleep)
                self.__processedCount += 1
        except Exception as ex:
            LogHelpers.critical(f'DepartmentProcessing: validateTDXAccountNames {str(ex)}')
        LogHelpers.displayHeader(f'{count} TDX accounts renamed')

    def deactivateInvalidTDXAccounts(self):
        #finds account listed in the TDX Department list but are not in the
        #Trident department lists
        #If the TDX Dept is not found, deactivate the TDX Account/Dept
        #Unable to delete the account through API endpoint
        count = 0
        tdxAcctList = self.__TDXDepart.getList()
        LogHelpers.displayHeader("Inactive account/departments")
        
        for acct in tdxAcctList.values():
            if not acct.getName() in self.__acctExceptions.keys():
                code = acct.getCode()
                if not self.__TridentDeptList.inList(code):
                    AccountAPI.deactivateAccount(acct)
                    acct.setIsActive(False)
                    count += 1
                    time.sleep(self.__sleep)
            self.__processedCount += 1
        LogHelpers.displayHeader(f'{count} TDX accounts deactivated')
 
    def getTDXAccountList(self):
        badCode = 0
        badCount = 0
        noCodeCount = 0
        badAccount = False
        goodCount = 0
        runningCount = 0
        inActiveCount = 0

        TDXList = {}
        TDXAcctJsonList = AccountAPI.getTDXAccountList()

        LogHelpers.displayHeader("Bad TDX Accounts")
        try:
            for acct in TDXAcctJsonList:
                code = acct['Code']
                name = acct['Name']
                acctID = acct['ID']
                isActive = acct['IsActive']
                if isActive:  #don't process inactive accounts, will check for consistency in createNewDepartments
                    if code:
                        if code in TDXList.keys():#checks to see if the code is already in the list, if so there is duplicate code in TDX
                            badAccount = True
                        else: 
                            TDXList[code] = Dept(code, name, acctID, isActive)
                            goodCount += 1
                            badAccount = False
                    elif (name and isActive) and (not name in self.__acctExceptions.keys()):
                            #have an active TDX acct with no code
                            badAccount = False
                            self.__NoCodeList[acctID] = Dept(code, name, acctID, isActive)
                            noCodeCount += 1
      
                    if badAccount: #TDX accounts with no code
                        if not name in self.__acctExceptions.keys():
                            badCount += 1
                            tridentDept =  self.__TridentDeptList.find(code)
                            if not tridentDept is None:
                                if code in TDXList.keys():
                                    del TDXList[code]  #code and department name don't match, delete and reset
                                TDXList[code] = tridentDept 
                                badDept = Dept(code, name, acctID, isActive)
                            else:
                                badCode -= 1 #Not a trident department, will need to deactivate in TDX
                                badDept = Dept(badCode, name, acctID, isActive)
                            self.__BadTDXList.add(badDept)
                            LogHelpers.warning(f'Account Name: {name}, Code: {code} is a BAD account')
                else:
                    inActiveCount += 1
        except Exception as ex:
            LogHelpers.critical(f'DepartmentProcessing: getTDXAccountList: {str(ex)}')
        LogHelpers.displayHeader("End Bad TDX Accounts")

        totalCount = (goodCount + badCount + noCodeCount) + len(self.__acctExceptions)
        output = f'Good TDX Accounts: {goodCount}\nBad TDX Accounts: {badCount}\nNo Code Accounts: {noCodeCount}\nExempt Accounts: {len(self.__acctExceptions)} \nTotal ValidAccounts: {totalCount}\nTotal Inactive Accounts: {inActiveCount}'
        LogHelpers.displayHeader(output)

        self.__TDXDepart.setList(TDXList)




