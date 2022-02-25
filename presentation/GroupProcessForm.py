from tkinter import *
from tkinter import ttk;
from tkinter import filedialog as fd
from presentation.BaseForm import BaseForm
from presentation.FormStyles import FormStyles as fr
from helpers.StringHelpers import StringHelpers as strHelp
from model.people.GroupAPI.GroupAPIMethods import GroupAPIMethods
from model.people.GroupInfo import GroupInfo
from model.people.GroupProcessing import GroupProcessing
from helpers.LogHelpers import LogHelpers
class GroupProcessForm(BaseForm):
    """description of class"""

    logFile = 'groups\\groupInfo'

    def __init__(self, window, formTitle):
        super().__init__(window, formTitle)
        super().setLogFile(self.logFile)

    def buildDirections(self):
        super().buildDirections()
        try:
            self.directions['text'] = "Provide the group name and group ID"
        except Exception as ex:
            message = f'MainForm-buildDirections: {str(ex)}'
            print(message)

    def buildGrid(self):
        super().buildGrid()
        self.closeButton = ttk.Button(self.opFrame2, text="Close Group Processing", command=self.window.destroy, style='My.TButton')
        self.closeButton.grid(row=0, column=1, sticky=E)

        self.groupList = GroupAPIMethods.getGroupList()
        self.selectedGroup = GroupInfo()


    def buildInput(self):

        self.lblName = ttk.Label(self.opFrame1, text="Select Group Name", style='My.TLabel')
        self.lblName.grid(row=1, column=0, sticky=W)
        self.name=StringVar()

        self.nameSelect = ttk.Combobox(self.opFrame1, 
                                       textvariable=self.name,
                                       state='readonly',
                                       style='My.TCombobox', 
                                       width=40)
        self.nameSelect.grid(row=2, column=0, stick=W)

        strList = ['']
        for id in self.groupList:
            strList.append(self.groupList[id].getName())
        self.nameSelect['values'] =  strList

        self.nameSelect.bind("<<ComboboxSelected>>", self.setNameSelect)

        self.lblGroupID = ttk.Label(self.opFrame1, text="Group ID", style='My.TLabel')
        self.lblGroupID.grid(row = 3, column=1, sticky=E)

        self.btnGetFile = ttk.Button(self.opFrame1, text="Select the file to import",
                                     command=self.getFile,
                                     style='My.TButton')
        self.btnGetFile["state"] = DISABLED
        self.btnGetFile.grid(row=4, column=0, sticky=W)

        self.lblFileName = ttk.Label(self.opFrame1, text="File Name", style='My.TLabel')
        self.lblFileName.grid(row=5, column=0, sticky=W)

        self.btnProcess = ttk.Button(self.opFrame2, text="Process Group", 
                                     command=self.processLawGroup, 
                                     style='My.TButton')
        self.btnProcess["state"] = DISABLED
        self.btnProcess.grid(row=0, column=0, sticky=W)

    def setNameSelect(self, event):
        theGroup = None
        for id in self.groupList: 
            grp = self.groupList[id]
            if grp.getName() == self.name.get():
                self.lblGroupID['text'] = str(grp)
                self.selectedGroup = grp
                self.btnGetFile["state"] = NORMAL
                self.btnProcess['text'] = "Process " + grp.getName() + " Group"
                break

    def getFile(self):
        self.fileName = fd.askopenfilename()
        self.lblFileName['text'] = "Filename: .../" + strHelp.getFileName(self.fileName)
        self.btnProcess["state"] = NORMAL
        self.window.focus_force()


    def processLawGroup(self):
        LogHelpers.displayHeader(f'Start {self.selectedGroup.getName()} group processing')
        studentGroup = GroupInfo(self.selectedGroup.getName(), self.selectedGroup.getID(), True)
        law = GroupProcessing(studentGroup, self.fileName, super().getUseSandBox())
        law.processGroupMembers()
        LogHelpers.displayHeader(f'End {studentGroup.getName()} group processing')

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

   



