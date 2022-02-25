from tkinter import Tk
from tkinter import ttk;
from helpers.LogHelpers import LogHelpers as log
from presentation.MainForm import MainForm
from presentation.GroupProcessForm import GroupProcessForm

def main():
    showMainForm()

def showMainForm():
    root = Tk()
    mainForm = MainForm(root, "TDX API Operations Console")
    root.mainloop()


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print(ex)






