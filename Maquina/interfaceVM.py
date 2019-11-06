# Interface Virtual Machine (TkInter)
# Group:
# Agostinho Sanches de Araújo	RA: 16507915
# Pedro Andrade Caccavaro		RA: 16124679

from tkinter import *
from tkinter import filedialog as tkFileDialog

class Example(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
        self.initUI()


    def initUI(self):
        self.parent.title("Virtual Machine")
        self.parent.configure(background="darkgray")

        widget1 = Frame(self.parent, borderwidth=2, width=680, height=430, bg="darkgray", relief="ridge")
        widget1.place(x=10,y=10)

        widget2 = Frame(widget1, borderwidth=1, width=500, height=250, bg="darkgray", relief="raised")
        widget2.place(x=10,y=10)

        Label(widget2, text="Instructions to be executed by the Virtual Machine", bg="darkgray", fg="darkblue", font="none 10 italic bold").place(x=90,y=10)

        widget7 = Frame(widget2, borderwidth=2, width=475, height=195, bg="white", relief="sunken")
        widget7.place(x=10,y=40)

        widget3 = Frame(widget1, borderwidth=1, width=145, height=405, bg="darkgray", relief="raised")
        widget3.place(x=520,y=10)

        Label(widget3, text="Stack Contents", bg="darkgray", fg="darkblue", font="none 10 italic bold").place(x=20,y=10)

        widget8 = Frame(widget3, borderwidth=2, width=120, height=350, bg="white", relief="sunken")
        widget8.place(x=10,y=40)

        widget4 = Frame(widget1, borderwidth=1, width=180, height=145, bg="darkgray", relief="raised")
        widget4.place(x=10,y=270)

        Label(widget4, text="Input Window", bg="darkgray", fg="darkblue", font="none 10 italic bold").place(x=40,y=10)

        widget9 = Frame(widget4, borderwidth=2, width=155, height=90, bg="white", relief="sunken")
        widget9.place(x=10,y=40)

        widget5 = Frame(widget1, borderwidth=1, width=180, height=145, bg="darkgray", relief="raised")
        widget5.place(x=200,y=270)

        Label(widget5, text="Output Window", bg="darkgray", fg="darkblue", font="none 10 italic bold").place(x=40,y=10)

        widget10 = Frame(widget5, borderwidth=2, width=155, height=90, bg="white", relief="sunken")
        widget10.place(x=10,y=40)

        widget6 = Frame(widget1, borderwidth=1, width=120, height=145, bg="darkgray", relief="raised")
        widget6.place(x=390,y=270)

        Label(widget6, text="Break Point's", bg="darkgray", fg="darkblue", font="none 10 italic bold").place(x=15,y=10)

        widget11 = Frame(widget6, borderwidth=2, width=95, height=90, bg="white", relief="sunken")
        widget11.place(x=10,y=40)

        Button(self.parent, text="Continue", bg="darkgray", width=20).place(x=180,y=450)

        self.parent.title("File dialog")
        self.pack(fill=BOTH, expand=1)

        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Open", command=self.onOpen)
        menubar.add_cascade(label="File", menu=fileMenu)

        self.txt = Text(self)
        self.txt.pack(fill=BOTH, expand=1)


    def onOpen(self):

        ftypes = [('All files', '*')]
        dlg = tkFileDialog.Open(self, filetypes = ftypes)
        fl = dlg.show()

        if fl != '':
            text = self.readFile(fl)
            self.txt.insert(END, text)


    def readFile(self, filename):

        f = open(filename, "r")
        text = f.read()
        return text


def main():
    root = Tk()
    ex = Example(root)
    root.geometry("700x500")
    root.resizable(0, 0)
    root.mainloop()

if __name__ == '__main__':
    main()
