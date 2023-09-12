#
# Main file
#

import tkinter
import tkinter.messagebox
import xml.etree.ElementTree as ET

# Settings
fullscreen = False

# Application wnd class


class AppWnd:
    def loadDataFile():
        AppWnd.dataRoot = ET.parse('data.xml').getroot()
        return True

    def onOption():
        return True

    def addOption(text, idx):
        radioOpt = tkinter.Radiobutton(AppWnd.frameOpts, text=text, font=("Arial", 12),
                                       variable=AppWnd.option, value=idx, pady=10,
                                       command=AppWnd.onOption)
        radioOpt.pack(anchor="w", padx=40)
        return True

    def removeOptions():
        for child in AppWnd.frameOpts.winfo_children():
            child.destroy()
        return True

    def nextQn():
        AppWnd.removeOptions()
        AppWnd.option = tkinter.IntVar(AppWnd.frameOpts, -1)
        AppWnd.labelMainQn["text"] = AppWnd.dataTree.attrib["qn"]
        if("desc" in AppWnd.dataTree.attrib):
            AppWnd.labelMainQnDesc["text"] = AppWnd.dataTree.attrib["desc"]
            AppWnd.labelMainQnDesc.pack(fill="x")
        else:
            AppWnd.labelMainQnDesc["text"] = ""
            AppWnd.labelMainQnDesc.pack_forget()
        # Options
        idx = 0
        for child in AppWnd.dataTree:
            if("ans" in child.attrib):
                AppWnd.addOption(child.attrib["ans"], idx)
                idx = idx + 1
        # Show submit button
        if(idx > 0):
            tkinter.Button(AppWnd.frameOpts, text="Submit", fg="black", width=20, height=2,
                           command=AppWnd.onSubmit).pack(side="left", pady=40)
        return True

    def onSubmit():
        if(AppWnd.option.get() >= 0):
            AppWnd.dataTree = AppWnd.dataTree[AppWnd.option.get()]
            AppWnd.nextQn()
        else:
            tkinter.messagebox.showwarning("Warning",
                                           "Please select an answer!")
        return True

    def onRestart():
        AppWnd.dataTree = AppWnd.dataRoot
        AppWnd.nextQn()
        return True

    def launch():
        # Main window
        mainWnd = tkinter.Tk()
        mainWnd.title("ADS")
        if(fullscreen):
            mainWnd.wm_attributes('-fullscreen', 'true')
        else:
            mainWnd.geometry("800x600")
            # mainWnd.resizable(0, 0)

        # Title
        tkinter.Label(mainWnd, text="Automated Diagnosis System",
                      font=("Arial Black", 24), fg="dark blue", bg="#ffffcc").pack(fill="x")
        tkinter.Label(mainWnd, text="COPYRIGHT © 2019 National Health Coorporation",
                      font=("Arial", 8, "bold"), fg="#404040", bg="#ffffcc").pack(fill="x")
        tkinter.Canvas(mainWnd, bg="#202020", height=1,
                       highlightthickness=0).pack(fill="x")

        # Vertical spacer
        tkinter.Canvas(mainWnd, height=20, highlightthickness=0).pack(fill="x")

        # Main question
        textPadX = 20
        frameQn = tkinter.Frame(mainWnd)
        AppWnd.labelMainQn = tkinter.Label(frameQn, text="",
                                           font=("Arial", 18), fg="black", justify="left", anchor="w", padx=textPadX)
        AppWnd.labelMainQn.bind('<Configure>', lambda e:
                                AppWnd.labelMainQn.config(wraplength=mainWnd.winfo_width()-textPadX*2))
        AppWnd.labelMainQn.pack(fill="x")
        AppWnd.labelMainQnDesc = tkinter.Label(frameQn, text="",
                                               font=("Arial", 12), fg="#303030", justify="left", anchor="w", padx=textPadX)
        AppWnd.labelMainQnDesc.bind('<Configure>', lambda e:
                                    AppWnd.labelMainQnDesc.config(wraplength=mainWnd.winfo_width()-textPadX*2))
        AppWnd.labelMainQnDesc.pack(fill="x")
        frameQn.pack(fill="x")

        # Options
        AppWnd.frameOpts = tkinter.Frame(mainWnd, padx=textPadX, pady=50)
        AppWnd.frameOpts.pack(fill="x")

        # Bottom area
        frameBottom = tkinter.Frame(mainWnd)
        frameBottom.pack(fill="x", side="bottom")
        tkinter.Canvas(frameBottom, bg="#202020", height=1,
                       highlightthickness=0).pack(fill="x")
        frameBottomSub = tkinter.Frame(frameBottom, padx=10, pady=10)
        frameBottomSub.pack(fill="x", side="bottom")
        btnRestart = tkinter.Button(frameBottomSub, text="Restart", fg="red", width=20, height=2,
                                    command=AppWnd.onRestart)
        btnRestart.pack(side="left")
        btnQuit = tkinter.Button(frameBottomSub, text="Quit", fg="red", width=20, height=2,
                                 command=mainWnd.destroy)
        btnQuit.pack(side="right")

        # Load data file
        if(not AppWnd.loadDataFile()):
            tkinter.messagebox.showerror(
                "Data File Error", "Failed to load the data file!")
            return False

        # Set first question
        AppWnd.onRestart()

        # Continue running
        mainWnd.mainloop()

        return True


# Launch the application window
AppWnd.launch()
