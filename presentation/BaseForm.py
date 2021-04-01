from abc import ABC, abstractmethod
from tkinter import *
from tkinter import ttk
from pathlib import Path

from presentation.FormStyles import FormStyles as fr
class BaseForm(ABC):
    """description of class"""

    def __init__(self, window, formTitle):
        self.window = window
        self.window.title(formTitle)
        self.window.geometry(fr.formSize)
        self.imageFolder = Path("images")

        self.initializeForm()

    def initializeForm(self):
        self.createStyles()
        self.buildForm()
        self.buildGrid()
        self.buildDirections()
        self.buildInput()

    def createStyles(self):
        self.frame_style = ttk.Style()
        self.frame_style.theme_use('clam')

        #self.frmStyle = ttk.Style()
        #self.frmStyle.configure('TFrame',
        #                        background=fr.frameBackground)


        self.title_style = ttk.Style()
        self.title_style.configure("TLabel", 
                                   font=('arial', 12), 
                                   padding ='3, 3, 12, 12')

        self.directions_style = ttk.Style()
        self.directions_style.configure('Dir.TLabel', 
                                    font = ('arial', 12, 'bold', 'underline'),
                                    width = fr.directionWidth,
                                    foreground = fr.fontColor)

        self.btnStyle = ttk.Style()
        self.btnStyle.configure('My.TButton', 
                            font = ('arial', 12, 'bold', 'underline'),
                            width = fr.btnWidth,
                            padding ='5 5',
                            foreground = fr.fontColor)

        self.lblStyle = ttk.Style()
        self.lblStyle.configure('My.TLabel', 
                            font = ('arial', 12),
                            padding ='5 5',
                            foreground=fr.fontColor)


    def buildForm(self):
        
        self.window.rowconfigure(0, weight=1)
        self.window.rowconfigure(1, weight=5)
        self.window.rowconfigure(2, weight=1)

        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=1)
        self.window.columnconfigure(2, weight=1)

    @abstractmethod
    def buildDirections(self):
        #child class needs to update the text for the window title

        try:
            self.dirFrame = ttk.Frame(self.window)
            self.dirFrame.grid(row=0, column=0, sticky=(N,W,E,S))
            self.dirFrame.rowconfigure(0, weight=1)
            self.dirFrame.columnconfigure(0, weight=1)

            self.directions = ttk.Label(self.dirFrame, style='Dir.TLabel')

            self.aImage=PhotoImage(file=self.imageFolder/'logo.png')
            self.imgLabel = ttk.Label(self.dirFrame, image=self.aImage, text="UO")
           
            self.directions.grid(row=0, column=0, sticky=W)
            self.imgLabel.grid(row=0, column=1, sticky=W)

        except Exception as ex:
            message = f'Build Directions: {str(ex)}'
            print(message)

    @abstractmethod
    def buildGrid(self):
        try:
            self.opFrame1 = ttk.Frame(self.window)
            self.opFrame1['borderwidth']=2
            self.opFrame1['relief']='sunken'
            self.opFrame1.grid(row=1, column=0, sticky=(N,W,E,S))

            self.opFrame2 = ttk.Frame(self.window)
            self.opFrame2.grid(row=2, column=0, sticky=(N,W,E,S))
            self.opFrame2.columnconfigure(0, weight=1)
            self.opFrame2.rowconfigure(0,weight=1)

        except Exception as ex:
            message = f'buildGrid: {str(ex)}'
            print(message)

    @abstractmethod
    def buildInput(self):
        pass