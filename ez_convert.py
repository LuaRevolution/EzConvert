import tkinter as tk
from tkinter import filedialog
import os

# --- core
ESCAPE_DICTIONARY = {
    "\'": "\\\'",       # '
    "\"": "\\\"",       # "
    "\\": "\\\\",       # \
    "\n": "\\n",        # \n,
    "\r": "\\r",        # \r
    "\t": "\\t",        # \t
}


def convert_text(text:str, delete_newline=True):
    '''
    Converts text to python escape sequences, pritns and returns the result.
    delete_newline specifies whether the newline at the end of the result is deleted.
    >>>convert("'")
    \'
    >>>convert("\")
    \\
    >>convert("\",delete_newline=False)
    \\\n
    '''
    converted_text = ""
    for c in text:
        if c in ESCAPE_DICTIONARY:
            converted_text=converted_text+ESCAPE_DICTIONARY[c]
        else:
            converted_text=converted_text+c
    converted_text=converted_text[:-2]
    print("Converted:\n"+converted_text)
    return converted_text
# --- window
class EzConvertWindow:
    '''
    GUI for EzConvert. Root is a tk instance.
    '''
    def __init__(self,root):
        # setup
        self.master = root
        self.placeInCenter(700,400)
        self.master.title("EzConvert")
        self.file_path = ""
        self.version = 1.0

        # ui
        menuBar = tk.Menu(self.master) # menu bar
        fileMainMenu = tk.Menu(menuBar,tearoff=0) # file drop down
        fileSaveMenu = tk.Menu(fileMainMenu,tearoff=0) # file drop down
        convertMenu = tk.Menu(menuBar,tearoff=0) # file drop down
        # file
        fileMainMenu.add_command(label="Open",command=self.open_file)
        fileMainMenu.add_separator()
        fileSaveMenu.add_command(label="Save", command=self.save_file)
        fileSaveMenu.add_command(label="Save As", command=lambda: self.save_file(newFile=True))
        fileMainMenu.add_cascade(label="Save",menu=fileSaveMenu)

        menuBar.add_cascade(label="File",menu=fileMainMenu) # add cascading list to menubar
        # convert
        convertMenu.add_command(label="Convert",command=self.convert_from_textbox)
        convertMenu.add_separator()
        convertMenu.add_command(label="UnConvert",command=self.unconvert_from_textbox)
        menuBar.add_cascade(label="Conversion",menu=convertMenu) # add cascading list to menubar

        menuBar.add_command(label="About",command=self.about)
        self.master.config(menu=menuBar)

        self.outputArea = tk.Text(
            self.master,
            bg="#e6e6e6",
        )
        self.outputScroll = tk.Scrollbar(self.master, command=self.outputArea.yview)
        self.outputArea.configure(yscrollcommand=self.outputScroll.set)
        self.outputArea.pack(side=tk.LEFT, fill=tk.BOTH,expand=True)
        self.outputScroll.pack(side=tk.RIGHT,fill=tk.Y)
    def open_file(self):
        try:
            tempfilepath = filedialog.askopenfilename(initialdir = os.getcwd(),title = "Select file",filetypes = (("TXT files","*.txt"),("all files","*.*")))
            if tempfilepath != "":
                self.file_path = tempfilepath
            else:
                return "User canceled save"
        except Exception as e:
            print(e)
            return "User canceled save"

        file = open(self.file_path,"rt")
        text = file.read()
        file.close()
        self.pToOutput(text)
    def save_file(self,newFile=None):
        file = None
        openParam = ""
        if newFile is None:
            if self.file_path == "":
                newFile=True
            else:
                newFile=False
        if newFile == True:
            try:
                tempfilepath = filedialog.asksaveasfilename(initialdir = os.getcwd(),title = "Select file",defaultextension=".txt",filetypes = (("TXT files","*.txt"),("all files","*.*")))
                if tempfilepath == "":
                    return "User canceled save"
                else:
                    self.file_path = tempfilepath
            except FileNotFoundError:
                return "User canceled save"
            openParam = "x"
        else:
            openParam = "w"

        # open
        try:
            try:
                file = open(self.file_path,openParam)
            except FileNotFoundError:
                return "User canceled save"
        except FileExistsError:
            os.remove(self.file_path)
            try:
                file = open(self.file_path,openParam)
            except FileNotFoundError:
                return "User canceled save"
        file.write(self.outputArea.get("1.0",tk.END))
        file.close()
        self.createPopup(wtitle="Saved file",wdescription="File has been saved :)")
    def about(self):
        version_txt = "Version: "+str(self.version)
        creator_txt = "Writer: "+"Ian Marven"
        abt_txt = version_txt+"\n"+creator_txt
        self.createPopup(wtitle="About program",wdescription=abt_txt)
    def createPopup(self,wtype="message",wtitle="Popup",wdescription="Description",okfunc=None,yfunc=None,nfunc=None,oktext="Ok",ytext="Yes",ntext="No",xpos=None,ypos=None,nodestroy=False): # creates a popup
        #two types: message and yn
        top = tk.Toplevel(self.master)
        top.resizable(False,False)
        top.title(wtitle)
        self.placeInCenter(300,85,window=top,xpos=xpos,ypos=ypos)
        frame = tk.Frame(top)
        frame.pack(side=tk.TOP)
        bframe = tk.Frame(top)
        bframe.pack()

        desc = tk.Label(frame,text=wdescription)
        desc.configure(height=3)
        desc.pack()

        if wtype == "yn":
            ybutton = tk.Button(bframe,text=ytext,width=(len(ytext)*3))
            nbutton = tk.Button(bframe,text=ntext,width=(len(ytext)*3))
            ybutton.pack(side=tk.LEFT)
            nbutton.pack(side=tk.LEFT)
            if yfunc is None:
                def yfunc():
                    if nodestroy is False:
                        top.destroy()
                ybutton.configure(command=yfunc)
            else:
                def yfunc2():
                    yfunc()
                    if nodestroy is False:
                        top.destroy()
                ybutton.configure(command=yfunc2)
            if nfunc is None:
                def nfunc():
                    if nodestroy is False:
                        top.destroy()
                nbutton.configure(command=nfunc)
            else:
                def nfunc2():
                    nfunc()
                    if nodestroy is False:
                        top.destroy()
                nbutton.configure(command=nfunc2)
        else:
            button = tk.Button(frame,text=oktext,width=(len(oktext)*3))
            button.pack()
            if okfunc is None:
                def okfunc():
                    if nodestroy is False:
                        top.destroy()
                button.configure(command=okfunc)
            else:
                def okfunc2():
                    okfunc()
                    if nodestroy is False:
                        top.destroy()
                button.configure(command=okfunc2)
    def convert_from_textbox(self,output=True):
        input = self.outputArea.get("1.0",tk.END)
        conv = convert_text(input)
        if output == True:
            self.pToOutput(conv)
        return conv
    def unconvert_from_textbox(self):
        input = self.outputArea.get("1.0",tk.END)
        for k,v in ESCAPE_DICTIONARY.items():
            input = input.replace(v,k)
        self.pToOutput(input)
    def pToOutput(self,text): # print to output
        if self.outputArea == None:
            return False
        elif isinstance(self.outputArea, tk.Frame):
            return False
        self.outputArea.configure(state=tk.NORMAL)
        self.outputArea.delete(1.0, "end")
        self.outputArea.insert("end", text)
    def placeInCenter(self,width,height,window=None,place=True,xpos=None,ypos=None,geostring_only=False): #fixes x,y placement of window
        if window is None:
            window=self.master
        if xpos is not None and ypos is not None:
            x = xpos - (width //2)
            y = ypos - (height //2)
        else:
            x = (window.winfo_screenwidth() // 2) - (width //2)
            y = (window.winfo_screenheight() // 2) - (height //2)
        geostring = "{}x{}+{}+{}".format(width,height,x,y)
        if geostring_only:
            return geostring
        if place==True:
            window.geometry(geostring)
        else:
            window.geometry(geostring)


if __name__ == "__main__":
    root = tk.Tk()
    window = EzConvertWindow(root)
    root.mainloop()
