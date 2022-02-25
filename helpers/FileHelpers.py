import csv
import sys
import os
from os import path
from tkinter import *
from tkinter import ttk;
from tkinter import filedialog as fd
from model.people.Person import Person
from helpers.LogHelpers import LogHelpers
from helpers.StringHelpers import StringHelpers as strHelp

class FileHelpers:
    """Reads SCV File and stores people in people list"""

    filename = ''
   
    @classmethod
    def getLogFilePath(cls):
        return os.getcwd() + '\\' + 'logfiles'

    @classmethod
    def stripBadCharacters(cls, name):
        cleanString = ''
        bad_chars = [';', ':', '!', "*", '\\', '/']

        for i in bad_chars :
            cleanString = name.replace(i, '')

        return cleanString

    @classmethod
    def getFileName(cls):
        fileName = fd.askopenfilename()
        return fileName


   

    



