from tkinter import *
from tkinter import ttk
from model.people.GroupProcessing import GroupProcessing 
from model.api.Group import Group
from presentation.GroupProcessForm import GroupProcessForm
from presentation.BaseForm import BaseForm
from presentation.FormStyles import FormStyles as fr

class MainForm(BaseForm):
   
    def buildDirections(self):
        super().buildDirections()
        try:
            self.directions['text'] = "Select the operation"
        except Exception as ex:
            message = f'MainForm-buildDirections: {str(ex)}'
            log.critical(message)

    def buildGrid(self):
        super().buildGrid()
        self.closeButton = ttk.Button(self.opFrame2, text="Exit Control Panel", command=self.window.quit, style='My.TButton')
        self.closeButton.grid(row=0, column=1, sticky=E)

    def buildInput(self):
        self.btnLawSchool = ttk.Button(self.opFrame1, text="Process Law Student Group", 
                                     command=self.openGroupProcessing, 
                                     style='My.TButton')
        self.btnLawSchool.grid(row=0, column=0, sticky=W)

        self.space1 = ttk.Frame(self.opFrame1, style='Sp.TLabel')
        self.space1.grid(row=0, column=1)

        self.btnDepartment = ttk.Button(self.opFrame1, text="Process Departments", 
                                     command="", 
                                     style='My.TButton')
        self.btnDepartment.grid(row=0, column=2, sticky=W)

    def openGroupProcessing(self):
        childWindow = Toplevel()
        groupForm = GroupProcessForm(childWindow, "Process Law Student Group")

   

 


