import re
import datetime

class StringHelpers:
    """description of class"""

    @staticmethod
    def strip_end(text, suffix, removeLen):
        value = text
        try:
            if text.endswith(suffix):
                value = text[:len(text) - removeLen]
        except Exception as ex:
            print("StringHelpers: strip_end: " + ex)
        return value

    @staticmethod
    def splitString(theString, delimiter):
        return theString.split(delimiter)

    @staticmethod
    def getFileName(theString):
        return theString.split('/')[-1]


    @staticmethod
    def findSubString(smallStr, fullString):
  
        found = False
        try:
            if not (smallStr is None):
                strSearch = smallStr.strip()
                if len(strSearch) > 0:
                    rex = re.compile(f'\\b{strSearch}\\b')
                    result = rex.findall(fullString.strip())
                    if len(result) > 0:
                        found = True
        except Exception as ex:
            found = False
        finally:
            return found



    @staticmethod
    def findInString(string1, string2):
        found = False
        if len(string1) > 0 and len(string2) > 0:
            if len(string1) >= len(string2):
                smallStr = string2.strip()
                fullStr = string1.strip()
            else:
                smallStr = string1.strip()
                fullStr = string2.strip()
            if fullStr.startswith(smallStr):
                found = True

        return found

    @staticmethod
    def compareStrings(str1, str2):
        return str1.lower().strip() == str2.lower().strip()

    @staticmethod
    def isLeasedBuilding(uoLocNum, tdxLocNum):
        isLeased = False
        if tdxLocNum[-1].lower() == "l":
            tdxLoc = tdxLocNum[:-1]
            if tdxLoc == uoLocNum:
                isLeased = True
        elif uoLocNum[-1].lower() == "l":
            uoLoc = uoLocNum[:-1]
            if uoLoc == tdxLocNum:
                isLeased = True
        return isLeased

    @staticmethod
    def findExactString(string1, string2):
        found = False
        index = 0
        smallStr = ''
        fullStr = ''
        if len(string1) >= len(string2):
            smallStr = string2.strip()
            fullStr = string1.strip()
        else:
            smallStr = string1.strip()
            fullStr = string2.strip()
        try:
            if len(smallStr) > 0 and len(fullStr) > 0:
                for i in range(0, len(smallStr)):
                    ch=smallStr[i]
                    index = fullStr.index(str(ch), index, len(fullStr))
                    if index >= 0:
                        found = True
                        index += 1
                    else:
                        found = False
                        break
            else:
                found = False
        except Exception as ex:
            found = False

        return found

    @staticmethod
    def getDateTime():
        theDate = datetime.datetime.now()
        timeStr = theDate.strftime("%b_%d_%Y_%H_%M")
        return timeStr

