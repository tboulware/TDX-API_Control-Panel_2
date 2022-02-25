from helpers.LogHelpers import LogHelpers
from tkinter import *
from tkinter import ttk;
from tkinter import messagebox
from tkinter import filedialog as fd
from model.locations.LocationFileOps import LocationFileOps
class UOSpaceInformation(object):
    """Pulls the bldg location and rooms from the UO Spaces spreadsheets, one for buildings and one for rooms
       at the end of these processing the list of locations has all the valid rooms and thier locations
    """

    @classmethod
    def getBuildingList(cls, theList, fileName):
        #get the building list, but no room information
        LocationFileOps.getBuildingList(theList, fileName)

    @classmethod
    def getFullLocations(cls, theList, fileName):
        #get locations file, which contains building details
        LocationFileOps.openFullRoomList(theList, fileName)
       
    @classmethod
    def printList(cls):
        for key, value in self.__theList.items():
            print(f'{value}')

    @classmethod
    def addRoomToLocation(cls, bldgID, room):
        location = self.__theList(blgdID)
        if location is not None:
            location.addRoom(room)
        else:
           message = "LocationList: addRoomToLocation: " + str(room) + " not added to " + str(location)
           LogHelpers.critical(message)
           print(message)