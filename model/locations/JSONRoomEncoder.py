import json
from json import JSONEncoder
from model.locations.Room import Room

class JSONRoomEncoder(JSONEncoder):
    """description of class"""

    def default(self, object):
        if isinstance(object, Room):
            return object.__dict__
        else:
            return json.JSONEncoder.default(self, object)



