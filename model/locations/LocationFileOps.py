import csv
from genericpath import exists
import sys
import os
from os import path
from helpers.LogHelpers import LogHelpers
from helpers.StringHelpers import StringHelpers
from helpers.FileHelpers import FileHelpers
class LocationFileOps():
    
    locPath = '\\locations\\'


    @classmethod
    def openFullRoomList(cls, locationList, fileName):
        from model.locations.Location import Location
        from model.locations.Address import Address
        from model.locations.Room import Room

        #write a method to search the keys for the correct index
        bldgKey = 0  #this maps to the TDX External ID
        bannerIDKey = 1
        bldgNameKey = 2
        addressKey = 4
        rmIDKey = 17
        rmNameKey = 19
        floorKey = 13

        bldgCount = 0
        totalRoomCount = 0
        duplicateRooms = []
        try:
           if(path.exists(fileName)):
                LogHelpers.displayHeader("Getting UO Spaces data")
                with open(fileName, mode='r', encoding="utf-8") as csvfile:
                    csvReader = csv.DictReader(csvfile)
                    #there may be garbage characters in the CSV file so get the keys and access by position
                    keys = csvReader.fieldnames

                    for row in csvReader:
                        try:
                            bannerID = row[keys[bannerIDKey]].strip()
                            bldgNumber = row[keys[bldgKey]].strip()
                            bldgName = row[keys[bldgNameKey]].strip()
                            if not (bannerID in locationList):
                                aAddress = Address(row[keys[addressKey]])
                                aLocation = Location(-1, bannerID, bldgNumber, bldgName, aAddress, "uospaces")
                                locationList[bannerID] = aLocation
                                bldgCount += 1
                                print(f'{bldgCount}: {bannerID}: {bldgName}, number: {bldgNumber}')

                            roomID = row[keys[rmIDKey]]
                            rmName = row[keys[rmNameKey]]
                            floor = row['Floor']
                            
                            if locationList[bannerID].roomInList(rmName):
                                duplicateRooms.append((bannerID, bldgNumber, bldgName, roomID, rmName))
                            else:
                                room = Room(-1, roomID, rmName,floor )
                                locationList[bannerID].addRoom(room)
                                totalRoomCount += 1
                        except Exception as ex:
                             LogHelpers.critical(f'LocationFileOps: openFullRoomList:  {str(ex)}: {bldgNumber}')
                       
        except FileExistsError as ex:
            LogHelpers.critical(f'LocationFileOps: openFullRoomList:  {str(ex)}')
        except Exception as ex:
           LogHelpers.critical(f'LocationFileOps: openFullRoomList:  {str(ex)}')
        finally:
            LogHelpers.displayHeader('\tUO Spaces Location Information') 
            LogHelpers.info(f'Number of buildings found: {bldgCount}')
            LogHelpers.info(f'Number of rooms found: {totalRoomCount}')

            #sort by name
            sortedLocations = sorted(locationList.items(), key=lambda kv: kv[1])
            LocationFileOps.writeLocationListToFile(locationList, 'UO Space Locations')

            if len(duplicateRooms) > 0:
                LogHelpers.info(f'Number of UO Spaces Duplicate Rooms: {len(duplicateRooms)}')
                LocationFileOps.saveDuplicateRoomList(duplicateRooms, 'UOSpacesDuplicateRooms')
            else:
                LogHelpers.displayHeader('No UO Spaces duplicate rooms')

            LogHelpers.displaySeparator()

    @classmethod
    def saveDuplicateRoomList(cls, dupRoomList, fileName):
        cleanString = FileHelpers.stripBadCharacters(fileName)
        thefilename = FileHelpers.getLogFilePath() + cls.locPath + cleanString + "_" + StringHelpers.getDateTime() + ".csv"
        fields = ['Bldg', 'Name', 'BannerID', "Room#"]
        try:
            with open(thefilename, 'w', newline='', encoding='utf-8') as csvfile:
                csvWriter = csv.writer(csvfile)
                csvWriter.writerow(fields)
                for i, rm in  enumerate(dupRoomList):
                    csvWriter.writerow(rm)
        except Exception as ex:
            LogHelpers.critical("LocationFileOps: saveDuplicateRoomList: " + ex)

    @classmethod
    def writeLocationListToFile(cls, theList, fileName):
        cleanString = FileHelpers.stripBadCharacters(fileName)
        thefilename = FileHelpers.getLogFilePath() + cls.locPath + cleanString + "_" + StringHelpers.getDateTime() + ".csv"
        fields = ['ID', 'Banner ID', 'Building Number', 'Building Name', 'Address', 'Number Rooms', 'Number Assets', 'Number Tickets']
        try:
           with open(thefilename, 'w', newline='', encoding='utf-8') as csvfile:
                csvWriter = csv.writer(csvfile)
                csvWriter.writerow(fields)
                for key in theList:
                    loc = theList[key]
                    locID = str(loc.getID())
                    bldgNum = loc.getBuildingNumber()
                    bnID = loc.getBannerID()
                    name = loc.getName()
                    add = loc.getAddress().getStreet()
                    numberRooms = loc.getRoomCount()
                    numberAssets = loc.getAssetCount()
                    numTickets = loc.getTicketCount()
                    row = [locID, bnID, bldgNum, name, add, numberRooms, numberAssets, numTickets]
                    csvWriter.writerow(row)
        except Exception as ex:
            LogHelpers.critical("FileOperations: writeLocationListToFile: " + ex)

    @classmethod
    def writeRoomListToFile(cls, theList, fileName):
        fields = ['ID', 'external ID', 'room #']
        cleanStr = FileHelpers.stripBadCharacters(fileName)
        thefilename = FileHelpers.getLogFilePath() + cls.locPath + cleanStr + ".csv"
        try:
            with open(thefilename, 'w', newline='', encoding='utf-8') as csvfile:
                csvWriter = csv.writer(csvfile)
                csvWriter.writerow(fields)
                for key in theList:
                    rm = theList[key]
                    rmID = rm.getRoomID()
                    extID = rm.getExternalID()
                    num=rm.getName()
                    row = [rmID, extID, num]
                    csvWriter.writerow(row)
        except Exception as ex:
            LogHelpers.critical(f'LocatonFileOps: writeRoomListToFile: {ex}')
