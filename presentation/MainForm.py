from tkinter import *
from tkinter import ttk
from model.people.GroupProcessing import GroupProcessing 
from presentation.GroupProcessForm import GroupProcessForm
from presentation.LocationsProcessForm import LocationsProcessForm
from presentation.DepartmentProcessingForm import DepartmentProcessingForm
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
        self.btnGrpProcessing = ttk.Button(self.opFrame1, text="Process Group Membership", 
                                     command=self.openGroupProcessing, 
                                     style='My.TButton')
        self.btnGrpProcessing.grid(row=0, column=0, sticky=W)

        self.space1 = ttk.Frame(self.opFrame1, style='Sp.TLabel')
        self.space1.grid(row=0, column=1)

        self.btnDepartment = ttk.Button(self.opFrame1, text="Process Departments", 
                                     command=self.openDepartmentProcessing, 
                                     style='My.TButton')
        self.btnDepartment.grid(row=0, column=2, sticky=W)

        self.btnLocations = ttk.Button(self.opFrame1, text="Process Locations",
                                       command=self.openLocationsProcessing, 
                                       style='My.TButton')

        self.btnLocations.grid(row=0, column=3, sticky=W)

    def openGroupProcessing(self):
        childWindow = Toplevel()
        groupForm = GroupProcessForm(childWindow, "Process Group")

    def openLocationsProcessing(self):
        childWindow = Toplevel()
        locationForm = LocationsProcessForm(childWindow, "Process Locations")

    def openDepartmentProcessing(self):
        childWindow = Toplevel()
        deptForm = DepartmentProcessingForm(childWindow,"Process Departments")

  
