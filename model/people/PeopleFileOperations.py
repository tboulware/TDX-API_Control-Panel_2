import csv
import sys
import os
from model.people.Person import Person
from helpers.LogHelpers import LogHelpers
from helpers.StringHelpers import StringHelpers

class PeopleFileOperations(object):
    """description of class"""

    @classmethod
    def openPeopleList(cls, theList, fileName):
        try:
            count=0
            LogHelpers.displayHeader("People List")

            with open(fileName, mode='r') as csvfile:
                csvReader = csv.DictReader(csvfile)
                keys=csvReader.fieldnames
                for row in csvReader:
                    duckID = str(row[keys[0]])
                    fullName = str(row[keys[1]])
                    email = str(row[keys[2]])

                    #create the people objects and store in the list, the list has these three fields in this order
                    aPerson = Person(duckID, fullName, email)
                    theList[row["Email"]] = aPerson
                    count += 1
                LogHelpers.info(f'Number of people: {count}')
        except FileExistsError as f_err:
            LogHelpers.critical("FileOperations: openPeopleList: " + f_errex)
        except Exception as ex:
           LogHelpers.critical("FileOperations: openPeopleList: " + ex)
        return count
    


