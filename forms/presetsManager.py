import os
from tkinter import *
from tkinter import messagebox


class presetsManager(Toplevel):

    def __init__(self, master, titles):
        super(presetsManager, self).__init__(master=master)
        self.title("Presets Manager")
        self.geometry("145x195")
        self.mainPath = os.path.dirname(__file__)
        icon = os.path.join(self.mainPath, '../Icons/default_icon.ico')
        self.iconbitmap(icon)
        self.resizable(False, False)

        # ListBox
        var = Variable(value=titles)
        self.availablePresets = Listbox(self, listvariable=var, selectmode=EXTENDED, height=9)

        # Buttons
        self.deleteButton = Button(self, text="Delete", command=lambda: self.delete())
        self.loadButton = Button(self, text="Load", command=lambda: self.load())

        # Placements
        REG_LAYOUT = 5
        self.availablePresets.place(x=10, y=REG_LAYOUT)
        self.deleteButton.place(in_=self.availablePresets, relx=0, rely=1.05, relwidth=0.45)
        self.loadButton.place(in_=self.availablePresets, relx=0.5, rely=1.05, relwidth=0.45)

        self.passingData = None

        # Binds
        self.x, self.y = None, None
        self.bind("<ButtonPress-1>", self.dragWindow)
        self.bind("<ButtonRelease-1>", self.dropWindow)
        self.bind("<B1-Motion>", self.moveWindow)

    def load(self):
        selection = self.availablePresets.curselection()
        if len(selection) != 1:
            self.bell()
            return messagebox.showerror(message="You can only choose one preset to load!")
        self.passingData = self.availablePresets.get(selection[0])
        self.destroy()

    def delete(self):
        selection = self.availablePresets.curselection()
        if len(selection) == 0:
            return messagebox.showerror(message="You must choose at least one preset to delete")
        if messagebox.askyesno(message=f"Are you sure you want to delete {len(selection)} items?"):
            self.passingData = [self.availablePresets.get(i) for i in selection]
            self.destroy()

    def dragWindow(self, event):
        if isinstance(event.widget, Toplevel):
            self.x = event.x
            self.y = event.y

    def dropWindow(self, event):
        if isinstance(event.widget, Toplevel):
            self.x = None
            self.y = None

    def moveWindow(self, event):
        if isinstance(event.widget, Toplevel):
            deltax = event.x - self.x
            deltay = event.y - self.y
            x = self.winfo_x() + deltax
            y = self.winfo_y() + deltay
            self.geometry(f"+{x}+{y}")
