from abc import ABC, abstractmethod
from tkinter import *
class BaseForm(ABC):
    """description of class"""

    def __init__(self, window, formTitle):
        self.window = window
        self.formTitle = formTitle
        self.formSize = "800x600"

        self.padx = 25
        self.pady = 5
        self.btnH = 2
        self.btnW = 20

        self.frameW = 750
        self.frameH = 180
        self.frameBD = 1
        self.borderColor="green"
        self.frameCur = "arrow"
        self.frameHighLightBack = "black"
        self.frameHighlight = "green"
        self.frameHighThick = 0

        self.initializeForm()

    def initializeForm(self):
        self.buildForm()
        self.buildGrid()
        self.buildDirections()
        self.buildInput()

    def buildForm(self):
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        self.window.geometry(self.formSize)
        self.window.title(self.formTitle)

    def buildGrid(self):
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

        self.window.grid_rowconfigure(2, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

        self.opFrame1 = Frame(self.window, 
                             width=self.frameW, 
                             height=self.frameH,
                             cursor=self.frameCur, 

                             )
        self.opFrame1.grid(row=1, column=0, pady=self.pady, sticky=(N, E))
        self.opFrame1.propagate(0)

        self.opFrame2 = Frame(self.window, 
                             width=self.frameW, 
                             height=self.frameH,
                             cursor=self.frameCur, 
                             )
        self.opFrame2.grid(row=2, column=0, pady=self.pady, sticky=(N, E))
        self.opFrame2.propagate(0)

        self.opFrame3 = Frame(self.window, 
                             width=self.frameW, 
                             height=self.frameH,
                             cursor=self.frameCur, 
                             )
        self.opFrame3.grid(row=2, column=0, pady=self.pady, sticky=(N, E))
        self.opFrame3.propagate(0)

        self.closeButton = Button(self.window, text="Exit", 
                                  command=self.window.quit,
                                  width=self.btnW, 
                                  height=self.btnH)

        self.closeButton.grid(row=2, column=2, padx=self.padx, pady=self.pady, sticky=W)



    @abstractmethod
    def buildDirections(self):
        self.dirFrame = Frame(self.window, 
                              width=self.frameW, 
                              height=self.frameH,
                              borderwidth=self.frameBD,
                              highlightbackground=self.frameHighlight
                              )
        self.dirFrame.grid_rowconfigure(0, weight=1)
        self.dirFrame.grid_columnconfigure(0, weight=1)
        self.dirFrame.grid(row=0, column=0, columnspan=3, pady=self.pady, sticky=(N, W))

        self.directions = Label(self.dirFrame)
        self.directions.grid(row=0, 
                        column=0,
                        padx=self.padx, 
                        pady=self.pady,
                        sticky=(N, W))

        self.dirFrame.propagate(0)

    @abstractmethod
    def buildInput(self):
        pass