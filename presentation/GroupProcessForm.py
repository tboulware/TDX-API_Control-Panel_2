from tkinter import *
from tkinter import ttk;
from presentation.BaseForm import BaseForm
from presentation.FormStyles import FormStyles as fr
import re

class GroupProcessForm(BaseForm):
    """description of class"""

    def buildDirections(self):
        super().buildDirections()
        try:
            self.directions['text'] = "Provide the group name and group ID"
        except Exception as ex:
            message = f'MainForm-buildDirections: {str(ex)}'
            log.critical(message)

    def buildGrid(self):
        super().buildGrid()
        self.closeButton = ttk.Button(self.opFrame2, text="Close Group Processing", command=self.window.destroy, style='My.TButton')
        self.closeButton.grid(row=0, column=1, sticky=E)

    def buildInput(self):

        ttk.Label(self.opFrame1, text="Group ID", style='My.TLabel').grid(row=0, column=0, sticky=E)
        groupNumber = StringVar()
        idValidation = (self.window.register(self.validateGroupID), "%P")
        groupEntry = ttk.Entry(self.opFrame1, 
                               width=fr.largeText, 
                               textvariable=groupNumber)
        groupEntry.configure(validate="key", validatecommand = idValidation)

        groupEntry.grid(row=0, column=1, sticky=(W, E))

        ttk.Label(self.opFrame1, text="Group Name", style='My.TLabel').grid(row=1, column=0, sticky=E)
        groupNameValidation = (self.window.register(self.validateGroupName), "%P")
        nameEntry = StringVar()
        nameEntry = ttk.Entry(self.opFrame1, 
                               width=fr.largeText, 
                               textvariable=nameEntry)
        nameEntry.configure(validate="key", validatecommand = groupNameValidation)
        nameEntry.grid(row=1, column=1, sticky=(W, E))

        self.btnProcess = ttk.Button(self.opFrame1, text="Process Law Student Group", 
                                     command=self.processLawGroup, 
                                     style='My.TButton')
        self.btnProcess.grid(row=2, column=0, columnspan=2, sticky=(W, E))

    def processLawGroup():
        studentGroup = Group('/groups/18957/members', 'Law Students', 'StudentList.csv')
        law = GroupProcessing(studentGroup)
        law.processGroupMembers()
        print("Processing the group")

    def validateGroupID(self, input):
        isValid = False
        try:
            if input.isdigit():
                print("Key = " + str(input))
                isValid = True
            else:
                isValid = False
                print("Key = " + str(input))
        except Exception as ex:
            message = f'GroupProcessing: validateGroupName: {str(ex)}'
            log.critical(message)

        return isValid

    def validateGroupName(self, input):
        isValid = False
        try:
            if input.isalpha():
                print("Key = " + str(input))
                isValid = True
            else:
                isValid = False
                print("Key = " + str(input))
        except Exception as ex:
            message = f'GroupProcessing: validateGroupName: {str(ex)}'
            log.critical(message)

   



