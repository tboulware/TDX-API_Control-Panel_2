import requests
import json

class AdminAuth(object):
    """Access TDX admin to retrieve a sessions Bearer Token"""

    def __init__(self):
        self.__API_URL_ROOT = "https://service.uoregon.edu/TDWebApi/api"
        self.__BEARER_AUTH = "/auth/loginadmin"
        self.__BEID = "F0A527F4-5A42-45FB-8DB2-D6A8D1265CAA"
        self.__WEBKEY = "72F5CFDB-4FC0-4811-A378-99B33522024A"
        self.__HEADERS = {'Content-Type':'application/json'}
        self.__authorized = False
        self.__authorize()

    def __str__(self):
        return "Header: " + str(self.__HEADERS) + " Authorized: " + str(self.__authorized)
        

    def __authorize(self):
        sess = requests.Session()
        resp = sess.post(self.__API_URL_ROOT + self.__BEARER_AUTH,
                     data=json.dumps(
                         {'BEID': self.__BEID,
                          'WebServicesKey':  self.__WEBKEY},
                         ),
                     headers=self.__HEADERS
                     )
        bearer_token=resp.text.strip()
        if (len( bearer_token) > 0):
            self.__HEADERS['Authorization'] = 'Bearer ' + bearer_token
            self.__authorized = True
        else:
            assert bearer_token != "", "authorization failed"

    def getHeaders(self):
        return self.__HEADERS

    def isAuthorized(self):
        return self.__authorized

    def getURLRoot(self):
        return self.__API_URL_ROOT
