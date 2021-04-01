from tkinter import *
from model.people.GroupProcessing import GroupProcessing 
from model.api.Group import Group
from presentation.GroupProcessForm import GroupProcessForm
from presentation.BaseForm import BaseForm
class MainForm(BaseForm):
   
    def buildDirections(self):
        super().buildDirections()
        self.directions['text'] = "Select the operation"

    def buildInput(self):
        self.btnProcess = Button(self.opFrame1, text="Process Law Student Group", 
                                     command=self.openGroupProcessing, 
                                     width=self.btnW, 
                                     height=self.btnH)

        self.btnProcess.grid(row=0, column=0, padx=self.padx, pady=self.pady, sticky=(N, E))

    def openGroupProcessing(self):
        form = Tk()
        groupForm = GroupProcessForm(form, "Process Law Student Group")


   

 


