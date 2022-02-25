from model.locations.Location import Location
from model.locations.TDXLocationAPI import TDXLocationAPI
from model.locations.LocationFileOps import LocationFileOps 
from model.locations.LocationOperations import LocationOperations
from helpers.LogHelpers import LogHelpers


class my_class(object):
   
    #should only have to run this once in each environment
    @classmethod
    def updateTDXExternalID(cls, uoLocationsList, tdxLocationsList, tdxDuplicateList):
        validCount = 0
        updateCount = 0
        failedCount = 0
        extIDUpdateFailedList = {}
        updateTDX = False
        LogHelpers.displayHeader('Updating TDX ExtID with BannerID')
        try:
            for bannerID in uoLocationsList:
                found = False
                uoLoc = uoLocationsList[bannerID]
                tdxLoc = Location()
                updateTDX = False
                LogHelpers.displaySeparator()
                LogHelpers.info(f'Processing {uoLoc.getName()} for Ext ID update')
                if bannerID in tdxLocationsList:
                    found = True
                    LogHelpers.info(f'ExtID/BannerID for {uoLoc.getName()} is valid')
                    validCount += 1
                else:
                    bldgNum = uoLoc.getBuildingNumber()
                    if bldgNum in  tdxLocationsList.keys():
                        tdxLoc = tdxLocationsList[bldgNum]
                        updateTDX = True
                    else:
                        name = uoLoc.getName()
                        for loc in tdxLocationsList:  #take into account buildings may have same name but different building number
                            tmpLoc = tdxLocationsList[loc]
                            if name == tmpLoc.getName() and (bldgNum != tmpLoc.getBuildingNumber()) :
                                updateTDX = True

                    if updateTDX:
                        tdxLoc.setBannerID(uoLoc.getBannerID())
                        tdxLoc.setBuildingNumber(uoLoc.getBuildingNumber())
                        tdxLoc.setValidBannerID(True)
                        TDXLocationAPI.updateTDXLocationExtID(tdxLoc)
                        updateCount += 1
                        found = True
                        LogHelpers.info(f'{updateCount}: {tdxLoc.getName()} BannerID: {tdxLoc.getBannerID()} updated')

                if not found:
                    extIDUpdateFailedList[uoLoc.getBannerID] = uoLoc
                    failedCount += 1

            for name in tdxDuplicateList:
                tdxLoc = tdxDuplicateList[name]
                for bannerID in uoLocationsList:
                    if tdxLoc.getName() == uoLocationsList[bannerID].getName():
                        uoLoc = uoLocationsList[bannerID]
                        tdxLoc.setBannerID(uoLoc.getBannerID())
                        tdxLoc.setBuildingNumber(uoLoc.getBuildingNumber())
                        tdxLoc.setValidBannerID(True)
                        TDXLocationAPI.updateTDXLocationExtID(tdxLoc)
                        updateCount += 1
                        LogHelpers.info(f'ExtID updated for {tdxLoc.getName()} from {uoLoc.getBuildingNumber()} to {tdxLoc.getBannerID()}')
                        break

        except Exception as ex:
            LogHelpers.critical(f'LocationProcessing:updateTDXExternalID: {str(ex)}')

        finally:
            LogHelpers.displayHeader('TDX Location Update Summary total UO Spaces Locations: {locationCount}') 
            LogHelpers.info(f'Number of valid TDX BannerID Locations: {validCount}')
            LogHelpers.info(f'Number TDX Locations updated: {updateCount}')
            LogHelpers.info(f'Number TDX Locations not updated: {failedCount}')

            if failedCount > 0:
                 LocationFileOps.writeLocationListToFile(extIDUpdateFailedList, 'TDX ExtID Not Updated')
            LogHelpers.displaySeparator()





