import time
from model.locations.UOSpaceInformation import UOSpaceInformation
from model.locations.Location import Location
from model.locations.TDXLocationAPI import TDXLocationAPI
from model.locations.LocationFileOps import LocationFileOps 
from model.locations.LocationOperations import LocationOperations
from helpers.LogHelpers import LogHelpers

class LocationProcessing(object):
    """description of class"""

    def __init__(self, fileName, useSandBox):
        self.__fileName = fileName
        self.__useSandbox = useSandBox
        TDXLocationAPI.setUseSandBox(self.__useSandbox)

        self.__UOSpacesLocationList = {}
        self.__TDXLocationList = {}
        self.__TDXGhostList = {}
        self.__TDXArchiveList = {}
        self.__TDXAddList = {}
        self.__TDXUpdateList = {}
        self.__VerifyList = {}
        self.__duplicateIDList = {}

    def processLocations(self):

        UOSpaceInformation.getFullLocations( self.__UOSpacesLocationList, self.__fileName)
        TDXLocationAPI.getTDXLocationList(self.__TDXLocationList, self.__duplicateIDList)

        #self.updateTDXExternalID()

        self.findLocationsToAdd()
        self.findTDXGhostLocations()
        self.findLocationsToUpdate()

    
    def findTDXGhostLocations(self):
        #if a location is in the TDX list but NOT in the UO spaces list
        #record the TDX location but do nothing since the location
        #may be a record that was manually added and is in use
        #if no tickets or assets assigned, delete the location
        activeCount = 0
        archiveCount = 0
        found = False
        try:
            LogHelpers.displayHeader('GhostList: TDX Locations NOT in UO Spaces')
            for bannerID in self.__TDXLocationList:
                found = False
                tdxLoc = self.__TDXLocationList[bannerID]
                if bannerID in self.__UOSpacesLocationList:
                    found = True
                else:
                    #try to find by building 
                    for key in self.__UOSpacesLocationList:
                        uoLoc = self.__UOSpacesLocationList[key]
                        if LocationOperations.checkBuildingNumber(tdxLoc, uoLoc):
                            found = True
                            break

                if not found:  #then check if there are any tickets assigned
                    if tdxLoc.getTicketCount() <= 0 and tdxLoc.getAssetCount() <= 0:
                        TDXLocationAPI.setLocationToArchive(tdxLoc)
                        self.__TDXArchiveList[bannerID] = tdxLoc
                        archiveCount += 1
                    else:
                        self.__TDXGhostList[bannerID] = tdxLoc
                        activeCount += 1
        except Exception as ex:
                LogHelpers.critical(f'LocationProcessing:findTDXGhostLocations:  {ex}')

        finally:
            if len(self.__TDXGhostList) > 0:
                LogHelpers.info('Review file TDXGhostList.csv for ghost list')
                LocationFileOps.writeLocationListToFile(self.__TDXGhostList, 'TDXGhostList')
                LogHelpers.displayHeader(f'Number of active ghost buildings: {activeCount}')
            else:
                LogHelpers.info('No TDX Active Ghost Locations')
                LogHelpers.displaySeparator()

            if len(self.__TDXArchiveList) > 0:
                LogHelpers.info('Review TDX Location Archive List')
                LocationFileOps.writeLocationListToFile(self.__TDXArchiveList, 'TDXLocationArchiveList')
                LogHelpers.displayHeader(f'Number of archived buildings: {archiveCount}')
            else:
                LogHelpers.info('No TDX Active Ghost Locations')
                LogHelpers.displaySeparator()
      

    def findLocationsToUpdate(self):
        found = False
        updateCount = 0
        verifyCount = 0
        LogHelpers.displayHeader('Finding TDX Locations to Update:  TDX Record Inconsistent with UO Spaces')
        try:
             for bannerID in self.__UOSpacesLocationList:
                if not bannerID in self.__TDXAddList:
                    found = False
                    uoLoc = self.__UOSpacesLocationList[bannerID]
                    tdxLoc = Location()
                    #normal case, the location is in both the TDX and UO Space List
                    LogHelpers.displayHeader(f'Processing {uoLoc.getName()}')
                    if bannerID in self.__TDXLocationList:
                        found = True
                        tdxLoc = self.__TDXLocationList[bannerID]
                        #check if attributes and rooms are consistent
                        if not (uoLoc == tdxLoc):
                            tdxLoc.setUOLocation(uoLoc)
                            #TDXLocationAPI.updateLocation(tdxLoc)
                            self.__TDXUpdateList[bannerID] = tdxLoc

                            updateCount += 1
                            LogHelpers.info(f'\tUpdate TDX Location: {tdxLoc.getName()}, ExtID: {tdxLoc.BannerID()}')
                    else:
                        self.__VerifyList[bannerID] = uoLoc
                        verifyCount += 1

        except Exception as ex:
                LogHelpers.critical(f'LocationProcessing:findLocationsToUpdate: {str(ex)}')
        finally:
            if len(self.__TDXUpdateList) > 0:
                LocationFileOps.writeLocationListToFile(self.__TDXUpdateList, 'TDXLocationUpdateList')
                LogHelpers.displayHeader('TDX Locations to update:  Inconsistent between UO Spaces and TDX')        
                LogHelpers.info(f'Number of locations to update: {len(self.__TDXUpdateList)}')
                LogHelpers.displaySeparator()
            else:
                LogHelpers.info('No TDX Locations to update')
                LogHelpers.displaySeparator()

            if len(self.__VerifyList) > 0:
                LocationFileOps.writeLocationListToFile(self.__VerifyList, 'TDXLocationVerifyList')
                LogHelpers.displayHeader('TDX Locations to verify:  Location in UO Spaces but need to verify in TDX')        
                LogHelpers.info(f'Number of locations to verify: {len(self.__VerifyList)}')    
                LogHelpers.displaySeparator()
            else:
                LogHelpers.info('No UO Locations Locations to verify in TDX')
                LogHelpers.displaySeparator()

        return found

    def findLocationsToAdd(self):
        addCount = 0
        found = False
        LogHelpers.displayHeader('Finding TDX Locations to Add:  Locations in UO Spaces not in TDX Locations')
        try:
             for bannerID in self.__UOSpacesLocationList:
                found = False
                uoLoc = self.__UOSpacesLocationList[bannerID]
                if bannerID in self.__TDXLocationList:
                    found = True
                else:
                    #try to find building id
                    for key in self.__TDXLocationList:
                        tdxLoc = self.__TDXLocationList[key]
                        if LocationOperations.checkBuildingNumber(tdxLoc, uoLoc):
                            tdxLoc.setBannerID(uoLoc.getBannerID())
                            TDXLocationAPI.updateTDXLocationExtID(tdxLoc)
                            found = True
                            break
                if not found:
                    self.__TDXAddList[bannerID] = uoLoc
                    TDXLocationAPI.addLocation(uoLoc)
                    addCount += 1

        except Exception as ex:
                LogHelpers.critical(f'LocationProcessing:findAddList: {str(ex)}')

        finally:
            if len(self.__TDXAddList) > 0:
                #add location including the room
                LogHelpers.info(f'{addCount} rooms added')
                LocationFileOps.writeLocationListToFile(self.__TDXAddList, 'UOLocationsToAdd')
            else:
                LogHelpers.info(f'No locations added')
            LogHelpers.displaySeparator()


    def resetExternalID(self):  #will be deleted after testing
        updateTDX = False
        updateCount = 0
        LogHelpers.displayHeader('resetExternalID: Reset TDX Location Ext ID to Building Number')
        try:
            for bannerID in self.__TDXLocationList:
                tdxLoc =  self.__TDXLocationList[bannerID]
                updateTDX = False
                if bannerID in self.__UOSpacesLocationList:
                    updateTDX = True
                    uoLoc = self.__UOSpacesLocationList[bannerID]

                else:
                    #try to find by building 
                    for key in self.__UOSpacesLocationList:
                        uoLoc = self.__UOSpacesLocationList[key]
                        if LocationOperations.checkBuildingNumber(tdxLoc, uoLoc):
                            updateTDX = True
                            break

                if updateTDX:
                    tdxLoc.setBannerID(uoLoc.getBannerID())
                    tdxLoc.setBuildingNumber(uoLoc.getBuildingNumber())
                    TDXLocationAPI.resetTDXLocationExtID(tdxLoc)
                    updateCount += 1
            
        except Exception as ex:
            LogHelpers.critical(f'LocationProcessing:resetExternalID:  {ex}')

        finally:
            if updateCount > 0:
                LogHelpers.info(f'{updateCount} locations updated')
                LocationFileOps.writeLocationListToFile(self.__TDXLocationList, 'TDX Location ExtIDs Updated')