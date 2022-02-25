import json

class Room(object):
    """description of class"""

    def __init__(self, rmID ='', extID = '', roomName='', floor=''):
        self.__ID = rmID
        self.__externalID = extID
        self.__name = roomName
        self.__floor = floor
        self.__valid = True
        self.__numberAssets = 0

    def __iter__(self):
        yield from {
            "externalID": self.__externalID,
            "name": self.__name, 
            "floor": self.__floor
        }. items()

    def __str__(self):
        return json.dumps(dict(self), ensure_ascii=False)

    def __repr__(self):
        return self.__str__()

    def to_json(self):
        jsonStr = f'"ExternalID:" \"{ self.__externalID}\", "Name:" \"{self.__name}\", "Floor:", \"{self.__floor}\"'

        return jsonStr

    def __eq__(self, other):
        return self.__name == other.__name

    def __lt__(self, other):
        return self.__name < other.__name
    
    def setRoomID(self, rmID):
        self.__ID = rmID

    def getRoomID(self):
        return self.__ID

    def getExternalID(self):
        return self.__externalID

    def setExternalID(self, value):
        self.__externalID = value

    def getName(self):
        return self.__name

    def setName(self, value):
        self.__name = value

    def setFloor(self, value):
        self.__floor = value

    def getFloor(self):
        return self.__floor

    def setValid(self, value):
        self.__valid  = value

    def getValid(self):
        return self.__valid 

    def getNumberAssets(self):
        return self.__numberAssets

    def setNumberAssets(self, numAssets):
        self.__numberAssets = numAssets




