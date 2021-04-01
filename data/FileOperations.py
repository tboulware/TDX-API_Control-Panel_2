import csv
import sys
import os
from os import path
import logging
from model.people.Person import Person


class FileOperations:
    """Reads SCV File and stores people in people list"""

    filename = ''

    @classmethod
    def openPeopleList(cls, theList, fileName):
        cls.filename = fileName
        try:
            count=0
            if (path.exists(cls.filename)):
                with open(cls.filename, mode='r') as csvfile:
                    csvreader = csv.DictReader(csvfile)
                   
                    for row in csvreader:
                       #create the people objects and store in the list, the list has these three fields in this order
                       aPerson = Person(row["DuckID"], row["FullName"], row["Email"])
                       theList[row["Email"]] = aPerson
                       count += 1
                    print(f'Number of people: {count}')
                    print('_______________________________________')
                    logging.info('Fields:' + ', '.join(field for field in csvreader.fieldnames)) 
                    logging.info(f'Number of people: {count}')
            else:
                raise FileExistsError("File does not exist")
        except FileExistsError as f_err:
            print("FileOperations: openPeopleList (file doesn't exist): " + f_errex.message)
            logging.critical("FileOperations: openPeopleList: " + ex.message)
        except Exception as ex:
           print("FileOperations: openPeopleList: " + ex.message)
           logging.critical("FileOperations: openPeopleList: " + ex.message)
        return count

   

    



