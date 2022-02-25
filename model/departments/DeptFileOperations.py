import csv
import sys
import os
from os import path
import logging
from model.departments.Dept import Dept
from helpers.LogHelpers import LogHelpers
from helpers.StringHelpers import StringHelpers

class DeptFileOperations(object):
    """description of class"""

    """Reads SCV File and stores people in department list"""

    filename = ''

    @classmethod
    def writeFile(cls, theList, fileName):
        count = 0
        cls.fileName = fileName + "_" + StringHelpers.getDateTime()
        try:
            saveFile = open(cls.fileName, mode='w')
            for acct in theList:
                saveFile.write(str(acct) + '\n')
                count += 1
        except FileExistsError as f_err:
            LogHelpers.critical(f'DeptFileOperations: writeFile: " {f_err.message}')
        except Exception as ex:
            LogHelpers.critical(f'DeptFileOperations: writeFile: " {ex.message}')
        else:
            if not saveFile.closed:
                saveFile.close
                LogHelpers.info(f'{count} TDX original ACCT records saved in {fileName}')
            else:
                LogHelpers.warning(f'{fileName} TDX original ACC records NOT saved')


    @classmethod
    def openDepartmentFile(cls, theList, fileName):
        cls.filename = fileName 
        try:
            count=0
            if (path.exists(cls.filename)):
                with open(cls.filename, mode='r') as csvfile:
                    csvreader = csv.DictReader(csvfile)
                    for row in csvreader:
                       #create the objects and store in the list
                       aDept = Dept(row["GWRODIR_DIR_ID"], row["GWBTDIR_DESC"])
                       theList[row["GWRODIR_DIR_ID"]] = aDept
                       count += 1
                    LogHelpers.info("____________________________________________")
                    LogHelpers.info("Trident Department Information")
                    LogHelpers.info('Fields:' + ', '.join(field for field in csvreader.fieldnames)) 
                    LogHelpers.info(f'Number of Trident departments: {count}')
                    LogHelpers.info("____________________________________________")
            else:
                raise FileExistsError("File does not exist")
        except FileExistsError as f_err:
            LogHelpers.critical(f'DeptFileOperations: openDepartmentFile:  {f_err.message}')
        except Exception as ex:
            LogHelpers.critical(f'DeptFileOperations: openDepartmentFile: " {ex.message}')
        return count
    
