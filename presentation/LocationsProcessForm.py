from tkinter import *
from tkinter import ttk;
from tkinter import filedialog as fd
from presentation.BaseForm import BaseForm
from presentation.FormStyles import FormStyles as fr
from helpers.StringHelpers import StringHelpers as strHelp
from model.locations.LocationProcessing import LocationProcessing
from helpers.LogHelpers import LogHelpers

class LocationsProcessForm(BaseForm):
    """description of class"""

    logFile = 'locations\\locationInfo'
    def __init__(self, window, formTitle):
        super().__init__(window, formTitle)
        super().setLogFile(self.logFile)
     
    def buildDirections(self):
        super().buildDirections()
        try:
            self.directions['text'] = "Select the UO Spaces Building List (no rooms)"
        except Exception as ex:
            message = f'MainForm-buildDirections: {str(ex)}'
            print(message)

    def buildGrid(self):
        super().buildGrid()
        self.closeButton = ttk.Button(self.opFrame2, text="Close Location Processing", command=self.window.destroy, style='My.TButton')
        self.closeButton.grid(row=0, column=1, sticky=E)

    def buildInput(self):

        self.btnGetFile = ttk.Button(self.opFrame1, text="Select the file to import",
                                     command=self.getFile,
                                     style='My.TButton')
        self.btnGetFile.grid(row=1, column=0, sticky=W)

        self.lblFileName = ttk.Label(self.opFrame1, text="File Name", style='My.TLabel')
        self.lblFileName.grid(row=2, column=0, sticky=W)

        self.btnProcess = ttk.Button(self.opFrame2, text="Process Locations", 
                                     command=self.processLocations, 
                                     style='My.TButton')
        self.btnProcess["state"] = DISABLED
        self.btnProcess.grid(row=0, column=0, sticky=W)

    def getFile(self):
        self.fileName = fd.askopenfilename()
        self.lblFileName['text'] = "Filename: .../" + strHelp.getFileName(self.fileName)
        self.btnProcess["state"] = NORMAL
        self.window.focus_force()

    def processLocations(self):
        LogHelpers.displayHeader(f'Start Location group processing')
        locationProcessing = LocationProcessing(self.fileName, super().getUseSandBox())
        locationProcessing.processLocations()   
        LogHelpers.displayHeader(f'End Location group processing')