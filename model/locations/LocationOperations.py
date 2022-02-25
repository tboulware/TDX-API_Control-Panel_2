from model.locations.LocationFileOps import LocationFileOps as fileOP
from helpers.LogHelpers import LogHelpers
from helpers.StringHelpers import StringHelpers
class LocationOperations():

    @classmethod
    def checkBannerID(cls, uoLoc, tdxLoc):
        isEqual = False
        if uoLoc.getBannerID().strip() == tdxLoc.getBannerID().strip():
            isEqual = True
        elif StringHelpers.findInString(uoLoc.getBannerID(), tdxLoc.getBannerID()):
            isEqual = True
        return isEqual

    @classmethod
    def checkBuildingNumber(cls, uoLoc, tdxLoc):
        isEqual = False
        if uoLoc.getBuildingNumber().strip() == tdxLoc.getBuildingNumber().strip():
            isEqual = True
        elif StringHelpers.findInString( uoLoc.getBuildingNumber(), tdxLoc.getBuildingNumber()):
            isEqual = True
        return isEqual

    @classmethod
    def checkName(cls, uoLoc, tdxLoc):
        isEqual = False
        if uoLoc.getName().strip().lower() == tdxLoc.getName().strip().lower():
            isEqual = True
            tdxLoc.setValidName(True)
        return isEqual

    @classmethod
    def checkAddress(cls, uoLoc, tdxLoc):
        isEqual = False
        if uoLoc.getAddress() == tdxLoc.getAddress():
            isEqual = True
            tdxLoc.setValidAddress(True)
        return isEqual

    @classmethod
    def checkRooms(cls, uoLoc, tdxLoc, uoRoomsNotInTDX, tdxRoomsNotInUOSpaces ):
        uoSpaceEqual = False
        tdxLocEqual = False

        try:
            if uoLoc.getRoomList() == tdxLoc.getRoomList():
                uoSpaceEqual = True
                tdxLocEqual = True
                tdxLoc.setValidRooms(True)
            else:
                #search for rooms that are in UOSpaces but not in TDX Locations--will need to add these TDX locations
                uoSpaceEqual = cls.checkMissingRooms("UO Spaces", uoLoc, "TDX Locations", tdxLoc, uoRoomsNotInTDX)
            
                #search for rooms that are in TDX locations, but not in UO Spacess--will leave this alone since they 
                #may be in use by assets (check)
                tdxLocEqual = cls.checkMissingRooms("TDX Locations", tdxLoc, "UO Spaces", uoLoc, tdxRoomsNotInUOSpaces)
                tdxLoc.setValidRooms(False)
        except Exception as ex:
            LogHelpers.critical(f'LocationOperations: checkRooms {str(ex)}')
            
        return tdxLocEqual and uoSpaceEqual

    @classmethod
    def checkMissingRooms(cls, source, sourceLoc, target, targetLoc, deviationList):  #order of arguments matters
        try:
            roomsEqual = True
            found = False
            for rm1 in sourceLoc.getRoomList():
                found = False
                for rm2 in targetLoc.getRoomList():
                    if rm1 == rm2:
                        rm1.setValid(True)
                        rm2.setValid(True)
                        found = True
                        break
                if not found:
                    rm1.setValid(False)
                    deviationList[rm1.getExternalID()] = rm1
                    roomsEqual = False

            if not roomsEqual:
                sourceLoc.setValidRooms(False)
                locFile = f'{sourceLoc.getBuildingNumber()}-{sourceLoc.getName()} {source} Rooms Not in {target}'
                fileOP.writeRoomListToFile(deviationList, locFile) 
                LogHelpers.info(f'{sourceLoc.getName()} room list not consistent with {target}')
        except Exception as ex:
            message = 'LocationOperations: checkMissingRooms ' + str(ex)
            LogHelpers.critical(message) 
        return roomsEqual

    @classmethod
    def copyUOLocation(cls,tdxLoc, UOLoc):
        #don't overwrite TDXLoc Id, which is the TDX record key value
        #used to update the TDX record
        found = False
        LogHelpers.displayDetail(f'Updating {tdxLoc.getName()}')
        try:
            tdxLoc.setBannerID(UOLoc.getBannerID())
            if not tdxLoc.getValidExtID():
                 tdxLoc.setExternalID(UOLoc.getBuildingNumber())

            if not tdxLoc.getValidName():
                tdxLoc.setName(UOLoc.getName())
           
            if not tdxLoc.getValidAddress():
                tdxLoc.setAddress(UOLoc.getAddress())

            if not tdxLoc.getValidRooms():
                #copy the room list, but leave any existing TDX rooms in place
                tdxLoc.__roomList.sort()
                UOLoc.__roomList.sort()
                if not tdxLoc.getRoomList() == UOLoc.getRoomList():
                    #add the UO Room to the TDX room list
                    #determine if room is in UO Spaces but not in TDX Locations
                    for rmUO in UOLoc.getRoomList():
                        found = False
                        for rmTDX in tdxLoc.getRoomList():
                            if rmTDX.getNumber() == rmUO.getNumber():
                                found = True
                                break
                        if not found:
                            #add the room to the room list
                            aRoom = Room(rmUO.getExternalID(), rmUO.getNumber())
                            aRoom.setValid(True)
                            tdxLoc.addRoom(aRoom)
                            #TDXLocationAPI.addRoom(tdxLoc, aRoom)
                            LogHelpers.info(f'\tAdding {rmUO} TDX record room list')
                            break
        except Exception as ex:
            message = f'Location:copyUOLocation'
            LogHelpers.critical(message)
            print(tdxLoc)
            print(UOLoc)
        finally:
            LogHelpers.displayHeader(f'End copy for {tdxLoc.getName()}')
            return found
