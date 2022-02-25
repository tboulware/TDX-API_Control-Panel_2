import json
from model.locations.JSONRoomEncoder import JSONRoomEncoder
from model.locations.LocationOperations import LocationOperations as locOP
from model.locations.Address import Address
from helpers.StringHelpers import StringHelpers
from helpers.LogHelpers import LogHelpers

class Location(object):
    """attributes for a location"""

    def __init__(self, id=-1, bannerID='', bldgNum='', name='', address='', source=''):
        self.__ID = id  #this is the TDX Key
        self.__bannerID = bannerID
        self.__blgdNumber = bldgNum  #External ID is the TDX mapping to UO Spaces Building Number
        self.__name = name
        self.__address = address
        self.__roomList = []
        self.__validBannerID = False
        self.__validblgdNumber = True
        self.__validName = True
        self.__validAddress = True
        self.__validRooms = True
        self.__tdxRoomsNotInUOSpaces = {}
        self.__uoRoomsNotInTDX = {}
        self.__source = source
        self.__UOLoc = None
        self.__ticketCount = 0
        self.__assetCount = 0
        self.__roomCount = 0


    def setID(self, value):
        self.__ID = value

    def getID(self):
        return self.__ID

    def setBannerID(self, bannerID):
        self.__bannerID = bannerID

    def getBannerID(self):
        return self.__bannerID

    def setValidBannerID(self, value):
        self.__validBannerID = value

    def setBuildingNumber(self, value):
        self.__blgdNumber = value

    def getBuildingNumber(self):
        return self.__blgdNumber
    
    def getRoomsNotInTDX(self):
        return self.__uoRoomsNotInTDX

    def getRoomsNotInUOSpaces(self):
        return self.__tdxRoomsNotInUOSpaces

    def __eq__(self, other):
        uoLoc = self
        tdxLoc = other
        try:
            #want to check all attributes of the room and mark them as invalid or valid
            tdxLoc.setValidBuildingNumber(locOP.checkBannerID(uoLoc, tdxLoc))
            tdxLoc.setValidName(locOP.checkName(uoLoc, tdxLoc))
            tdxLoc.setValidAddress(locOP.checkAddress(uoLoc, tdxLoc))
            tdxLoc.setValidRooms(locOP.checkRooms(uoLoc, tdxLoc, tdxLoc.getRoomsNotInTDX(), tdxLoc.getRoomsNotInUOSpaces()))
        except Exception as ex:
            LogHelpers.critical(f'Location __eq__: {str(ex)}')  
        return tdxLoc.isValid()

    def __lt__(self, other):
        return self.__name < other.__name

    def __str__(self):
        message = f'ExtID: {self.__blgdNumber}, BannerID: {self.__bannerID}: {self.__name}, {self.__address}, Room Count: {self.roomCount()}'
        return message

    def isValid(self):
        return self.__validblgdNumber and self.__validName and self.__validAddress and self.__validRooms


    def setName(self, value):
        self.__name = value

    def getName(self):
        return self.__name

    def setValidName(self, isValid):
        self.__validName = isValid

    def getValidName(self):
        return self.__validName

    def setAddress(self, value):
        self.__address = value

    def getAddress(self):
        return self.__address

    def setValidAddress(self, isValid):
        self.__validAddress = isValid

    def getValidAddress(self):
        return self.__validAddress

   
    def setValidBuildingNumber(self, isValid):
        self.__validblgdNumber = isValid

    def getValidBuildingNumber(self):
        return self.__validblgdNumber

    def setValidRooms(self, isValid):
        self.__validRooms = isValid

    def getValidRooms(self):
        return self.__validRooms

    def addRoom(self, room):
        self.__roomList.append(room)

    def addRoomList(self, roomList):
        self.__roomList = roomList

    def getRoomList(self):
        return self.__roomList

    def setRoomList(self, rmList):
        self.__roomList = rmList

    def getJSONRoomList(self):
         JsonRoomList = []
         for rm in self.__roomList:
             jsonStr = "{" + rm.to_json() + "}"
             JsonRoomList.append(jsonStr)

         return JsonRoomList


    def getSource(self, source):
        return self.__source

    def setTicketCount(self, numTickets):
        self.__ticketCount = numTickets

    def getTicketCount(self):
        return self.__ticketCount

    def roomInList(self, name):
        inList = False
        for rm in self.__roomList:
            if rm.getName() == name:
                inList = True
                break
        return inList

    def setRoomCount(self, rmCount):
        self.__roomCount = rmCount

    def getRoomCount(self):
        return self.__roomCount

    def setAssetCount(self, assetCount):
        self.__assetCount = assetCount

    def getAssetCount(self):
        return self.__assetCount


    def roomCount(self):
        return str(len(self.__roomList))

    def checkTDXExternalID(self, bannerID, address):
        isValid = False
        if (StringHelpers.isSubString(self.__blgdNumber, bannerID)):
            #double check that addresses ae the same
            if self.__address == address:
                isValid = True
        return isValid

    def locationStatus(self):
        status = f'\t {self.__blgdNumber}, {self.__name}'
        if self.__validblgdNumber:
            status += '\n\tBldg Number: valid'
        else:
            status += '\n\tBldg Numbe: not valid'

        if self.__validName:
            status += '\n\tName: valid'
        else:
            status += '\n\tName: not valid'

        if  self.__validAddress:
            status += '\n\tAddress: valid'
        else:
            status += '\n\tAddress: not valid'

        if self.__validRooms:
            status += '\n\tRooms: valid'
        else:
            status += '\n\tRooms: not valid'

        return status

    def setUOLocation(self, uoLoc):
        self.__UOLoc = uoLoc
        self.__validName = False
        self.__validName = False

    def getTDXRoomsNotInUOSpace(self):
        return self.__tdxRoomsNotInUOSpaces

    def getUORoomsNotInTDX(self):
        return self.__uoRoomsNotInTDX

                


