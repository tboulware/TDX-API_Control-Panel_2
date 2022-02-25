import requests
import json
import time
import csv
from os import path
from model.api.AdminAuth import AdminAuth
from model.locations.Address import Address
from model.locations.Location import Location
from model.locations.Room import Room
from model.locations.LocationFileOps import LocationFileOps
from helpers.LogHelpers import LogHelpers 
from helpers.FileHelpers import FileHelpers

class TDXLocationAPI(object):
    """description of class"""

    #chapman 7685
    #'/7942'  #Baker
    #lawarence 7680
    #friendly 7688

    #switch to production property value when running againist Production
    propertyID = 130174
    propertyName = 'BannerID'

    locationMethod = "/locations"
    sleep = 1.05
    locationCount = 0
    roomCount = 0
    auth = AdminAuth()

    @classmethod
    def setUseSandBox(cls, useSandbox):
        cls.auth.setUseSandbox(useSandbox)

    @classmethod
    def getTDXLocationList(cls, theList, dulplicateList):
        locationJSONList = []
        count = 0
        numberTickets = 0
        if cls.auth.isAuthorized():
            try:
                LogHelpers.displayHeader("Getting TDX Location data")
                url = cls.auth.getURLRoot() + cls.locationMethod 
                sess = requests.Session()
                sess.headers = cls.auth.getHeaders()
                resp = sess.get(url)
                if resp.ok:
                    locationJSONList = json.loads(resp.text)
                    for loc in locationJSONList:
                        tdxID = loc['ID']
                        name = loc['Name']
                        bannerID = loc['ExternalID']  #externalID maps to UO Spaces BannerID
                        street = loc['Address']
                        city = loc['City']
                        state = loc['State']
                        zipCode = loc['PostalCode']
                        aAddress = Address(street, city, state, zipCode)
                        location = Location(tdxID, bannerID, '', name, aAddress, "TDX")
                        cls.getLocationDetails(location)  #not all the details are returned with the get location list endpoint
                        if bannerID in theList.keys():
                            #don't know which of the duplicates is correct
                            tmpLoc = theList[bannerID]
                            if not tmpLoc.getName() in dulplicateList.keys():  #only add the first duplicate once
                                dulplicateList[tmpLoc.getName()] = tmpLoc
                            dulplicateList[name] = location
                            LogHelpers.warning(f'duplicate BannerID: {bannerID}: {name}')
                        else:
                            theList[bannerID] = location
                        count+=1
                        print(f'{count}: {bannerID}: {name}')
                else:
                     raise Exception("Location list not returned")
            except json.JSONDecodeError as jsonex:
                message = f'LocationAPI:getLocationList: {str(jsonex.doc)}'
                LogHelpers.critical(message)
            except Exception as ex:
                message = f'LocationAPI:getLocationList:  {str(ex)}'
                LogHelpers.critical(message)
        else:
            message = f'LocationAPI:getLocationList: not authorized'
            LogHelpers.critical(message)

        LogHelpers.displayHeader('TDX Location Information')
        LogHelpers.info(f'Number of buildings found: {count}')
        LogHelpers.info(f'Number of rooms found: {cls.roomCount}')     
        
        LocationFileOps.writeLocationListToFile(theList, 'TDX Locations')
        LogHelpers.displaySeparator()


    @classmethod
    def getLocationDetails(cls, location):
         if cls.auth.isAuthorized():
            try:
                url = cls.auth.getURLRoot() + cls.locationMethod + "/" + str(location.getID())
                sess = requests.Session()
                sess.headers = cls.auth.getHeaders()
                resp = sess.get(url)
                if resp.ok:
                    locationJSON = json.loads(resp.text)
                    location.setTicketCount(locationJSON['TicketsCount'])
                    location.setAssetCount(locationJSON['AssetsCount'])
                    location.setRoomCount(locationJSON['RoomsCount'])
                    location.setRoomList(locationJSON['Rooms'])
            except json.JSONDecodeError as jsonex:
                LogHelpers.critical(f'LocationAPI:getLocationDetails: {str(jsonex.doc)}')
            except Exception as ex:
                LogHelpers.critical(f'LocationAPI:getLocationDetails:  {str(ex)}')
               
    @classmethod
    def addLocation(cls, location):
        success = False
        if cls.auth.isAuthorized():
            try:
                time.sleep(cls.sleep) #API rate limited
                url = cls.auth.getURLRoot() + cls.locationMethod
                sess = requests.Session()
                sess.headers = cls.auth.getHeaders()
                payload = {'ExternalID': location.getBannerID(),
                           'Name': location.getName(),
                           'Address': location.getAddress().getStreet(),
                           'City': location.getAddress().getCity(),
                           'State': location.getAddress().getState(),
                           'PostalCode': location.getAddress().getZip(),
                           "Description": "UO Building Number: " + location.getBuildingNumber(),
                           'IsActive': True
                    }
                resp = sess.post(url, data = json.dumps(payload))
                if resp.ok:
                    #newly generated location with  TDX id
                    locJson =  json.loads(resp.text)
                    location.setID(locJson['ID'])
                    for rm in location.getRoomList():
                        cls.addTDXRoom(location, rm)
                    LogHelpers.info(f'{location.getName()} added')
                else:
                    LogHelpers.warning(f'{location.getName()} : not added')
                success = True
            except json.JSONDecodeError as jsonex:
                LogHelpers.critical(f'LocationAPI:addLocation: {str(jsonex.doc)}')
            except Exception as ex:
                LogHelpers.critical(f'LocationAPI:addLocation:  {str(ex)}')
        else:
            message = f'LocationAPI:addLocation: not authorized'
            LogHelpers.critical(message)

        return success

    @classmethod
    def addTDXRoom(cls, location, room):
        if cls.auth.isAuthorized():
            try:
                time.sleep(cls.sleep) #API rate limited
                url = cls.auth.getURLRoot() + cls.locationMethod + "/" + str(location.getID()) + "/rooms"
                req = requests.Session()
                req.headers = cls.auth.getHeaders()
                payload =  { "Name": room.getName(), 
                             "ExternalID": room.getExternalID(), 
                             "Floor": room.getFloor()
                            }
                resp = req.post(url, data=json.dumps(payload))
                if resp.ok:
                    LogHelpers.info(f'{location.getName()} room: {room.getName()} added')
                else:
                    LogHelpers.warning(f'{location.getName()} room: {location.getName()} NOT added, response: {resp}')
            except json.JSONDecodeError as jsonex:
                LogHelpers.critical(f'LocationAPI:addTDXRoom: {str(jsonex.doc)}')
            except Exception as ex:
                LogHelpers.critical(f'LocationAPI:addTDXRoom:  {str(ex)}')
        else:
            LogHelpers.critical(f'TDXLocationAPI: addRoom: not authorized')
            LogHelpers.info(f'{location.getName()} {room.getExternalID}: not added')

    @classmethod
    def deleteTDXRoom(cls, location, room):
         if cls.auth.isAuthorized():
            try:
                url = cls.auth.getURLRoot() + cls.locationMethod + "/" + str(location.getID()) + "/rooms/" + room.getRoomID()
                req = requests.Session()
                req.headers = cls.auth.getHeaders()
                resp = req.delete(url)
                if resp.ok:
                    LogHelpers.info(f'{location.getName()} room: {room.getName()} deleted')
                else:
                    LogHelpers.warning(f'{location.getName()} room: {room.getName()} NOT deleted')
            except json.JSONDecodeError as jsonex:
                LogHelpers.critical(f'LocationAPI:deleteTDXRoom: {str(jsonex.doc)}')
            except Exception as ex:
                LogHelpers.critical(f'LocationAPI:deleteTDXRoom:  {str(ex)}')
         else:
            LogHelpers.critical(f'TDXLocationAPI: deleteTDXRoom: not authorized')
            LogHelpers.info(f'{location.getName()} {room.getExternalID}: not deleted')


    @classmethod
    def setLocationToArchive(cls, location):
        if cls.auth.isAuthorized():
            try:
                url = cls.auth.getURLRoot() + cls.locationMethod + "/" + str(location.getID())
                req = requests.Session()
                req.headers = cls.auth.getHeaders()
                payload = { "Name": location.getName(),
                            "IsActive": False,
                            "ExternalID": location.getBuildingNumber(),
                            "Address": location.getAddress().getStreet(),
                            "City": location.getAddress().getCity(),
                            "State": location.getAddress().getState(),
                            "Zip": location.getAddress().getZip(),
                            "Attributes": 
                            [
                                {
                                    "ID": cls.propertyID,
                                    "Name": cls.propertyName,
                                    "Order": 0,
                                    "Value": location.getBannerID()
                                }
                            ]
                          }
                resp = req.put(url, data=json.dumps(payload))
                if resp.ok:
                    LogHelpers.info(f'{location.getName()} archived')
                else:
                    LogHelpers.warning(f'{location.getName()} not archived')

            except json.JSONDecodeError as jsonex:
                LogHelpers.critical(f'LocationAPI:setLocationToArchive: {str(jsonex.doc)}')
            except Exception as ex:
                LogHelpers.critical(f'LocationAPI:setLocationToArchive:  {str(ex)}')
        else:
            LogHelpers.critical(f'TDXLocationAPI: setLocationToArchive: not authorized')
            LogHelpers.info(f'{location.getName()} not archived')

    @classmethod
    def updateLocation(cls, location):
        if cls.auth.isAuthorized():
            try:
                url = cls.auth.getURLRoot() + cls.locationMethod + "/" + str(location.getID())
                req = requests.Session()
                req.headers = cls.auth.getHeaders()
                payload = { "Name": location.getName(),
                            "IsActive": True,
                            "ExternalID": location.getBuildingNumber(),
                            "Address": location.getAddress().getStreet(),
                            "City": location.getAddress().getCity(),
                            "State": location.getAddress().getState(),
                            "Zip": location.getAddress().getZip(),
                          }
                resp = req.put(url, data=json.dumps(payload))
                if resp.ok:
                    #remove any rooms listed in TDX location, but not listed in UO spaces
                    #if the TDX location has no assets
                    if len(location.getTDXRoomsNotInUOSpace()) > 0:
                        roomList = location.getTDXRoomsNotInUOSpace()
                        for rm in roomList:
                            if rm.getNumberAssets() <= 0:
                                cls.deleteTDXRoom(location, rm)
                    if len(location.getUORoomsNotInTDX() > 0):
                        roomList = location.getUORoomsNotInTDX()
                        for rm in roomList:
                            cls.addTDXRoom(location, rm)
                    LogHelpers.info(f'{location.getName()} updated: {location.getBannerID()}')
                else:
                    LogHelpers.warning(f'{location.getName()} not updated: {location.getBannerID()}')

            except json.JSONDecodeError as jsonex:
                LogHelpers.critical(f'LocationAPI:updateLocation: {str(jsonex.doc)}')
            except Exception as ex:
                LogHelpers.critical(f'LocationAPI:updateLocation:  {str(ex)}')
        else:
            LogHelpers.critical(f'TDXLocationAPI: updateLocation: not authorized')


    @classmethod
    def getTDXLocationFromFile(cls, theList):
        fileName = FileHelpers.getFileName()
        count = 0
        try:
            if (path.exists(fileName)):
                LogHelpers.displayHeader("Getting TDX Locations from File")
                with open(fileName, mode='r') as csvfile:
                    csvReader = csv.DictReader(csvfile)
                    keys = csvReader.fieldnames
                    for row in csvReader:
                        tdxID = row[keys[0]]
                        extID = row[keys[1]]
                        bannerID = row[keys[2]]
                        name = row[keys[3]]
                        address = row[keys[4]]
                        aAddress = Address(address)
                        location = Location(tdxID, extID, bannerID, name, aAddress, "TDX Files")
                        location.setRoomList(cls.getLocationRooms(tdxID))
                        if len(bannerID) > 0:
                            theList[bannerID] = location
                        else:
                            theList[extID] = location
                        count+=1
                        print(f'{count}', end=", ")
        except FileExistsError as ex:
            LogHelpers.critical(f'TDXLocationAPI: getTDXLocationFromFile:  {str(ex)}')
        except Exception as ex:
           LogHelpers.critical(f'TDXLocationAPI: getTDXLocationFromFile:  {str(ex)}')
        finally:
            LogHelpers.displayHeader('TDX Location Information from Files')
            LogHelpers.info(f'Number of buildings found from file: {count}')

    @classmethod
    def updateTDXLocationExtID(cls, location):
        if cls.auth.isAuthorized():
            try:
                url = cls.auth.getURLRoot() + cls.locationMethod + "/" + str(location.getID())
                req = requests.Session()
                req.headers = cls.auth.getHeaders()
                payload = { "Name": location.getName(),
                            "IsActive": True,
                            "ExternalID": location.getBannerID(),
                            "Address": location.getAddress().getStreet(),
                            "City": location.getAddress().getCity(),
                            "State": location.getAddress().getState(),
                            "Zip": location.getAddress().getZip(),
                            "Description": "UO Building Number: " + location.getBuildingNumber()
                          }
                time.sleep(cls.sleep) #API rate limited
                resp = req.put(url, data=json.dumps(payload))
                if not resp.ok:
                     LogHelpers.warning(f'{location.getName()}  external ID NOT set to: {location.getBannerID()}')                   

            except json.JSONDecodeError as jsonex:
                LogHelpers.critical(f'LocationAPI:updateBannerID: {str(jsonex.doc)}')
            except Exception as ex:
                LogHelpers.critical(f'LocationAPI:updateBannerID:  {str(ex)}')
        else:
            LogHelpers.critical(f'TDXLocationAPI: addRoom: not authorized')
            LogHelpers.info(f'{location.getName()} BannerID: {location.getBannerID()} added to TDX')


           