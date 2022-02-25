import os
import sys
from tkinter import *
from tkinter import ttk;
from tkinter import filedialog as fd
from presentation.BaseForm import BaseForm
from presentation.FormStyles import FormStyles as fr
from helpers.StringHelpers import StringHelpers as strHelp
from helpers.LogHelpers import LogHelpers
from model.departments.DepartmentProcessing import DepartmentProcessing

class DepartmentProcessingForm(BaseForm):
    """description of class"""

    logFile = 'departments\\deptInfo'

    def __init__(self, window, formTitle):
        super().__init__(window, formTitle)
        super().setLogFile(self.logFile)               
                       

    def buildDirections(self):
        super().buildDirections()
        try:
            self.directions['text'] = "Trident to TDX Department Update"
        except Exception as ex:
            message = f'MainForm-buildDirections: {str(ex)}'
            print(message)

    def buildGrid(self):
        super().buildGrid()
        self.closeButton = ttk.Button(self.opFrame2, text="Close Group Processing", command=self.window.destroy, style='My.TButton')
        self.closeButton.grid(row=0, column=1, sticky=E)

    def buildInput(self):
       

        self.btnGetFile = ttk.Button(self.opFrame1, text="Select the file to import",
                                     command=self.getFile,
                                     style='My.TButton')
        self.btnGetFile.grid(row=1, column=0, sticky=W)

        self.lblFileName = ttk.Label(self.opFrame1, text="File Name", style='My.TLabel')
        self.lblFileName.grid(row=2, column=0, sticky=W)

        self.btnProcess = ttk.Button(self.opFrame2, text="Process Departments", 
                                     command=self.processDepartments, 
                                     style='My.TButton')
        self.btnProcess["state"] = DISABLED
        self.btnProcess.grid(row=0, column=0, sticky=W)

    
    def getFile(self):
        self.fileName = fd.askopenfilename()
        self.lblFileName['text'] = "Filename: .../" + strHelp.getFileName(self.fileName)
        self.btnProcess["state"] = NORMAL
        self.window.focus_force()

    def processDepartments(self):
        LogHelpers.displayHeader(f'Start department processings')
        deptProcess = DepartmentProcessing(self.fileName, super().getUseSandBox())
        deptProcess.processDeparments()







