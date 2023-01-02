from tkinter import Menu, messagebox
from tkinter.ttk import Combobox

from forms.presetsManager import presetsManager
from configs.IPWidget import IPWidget
from configs.fileManager import fileManager


class Toolbar(Menu):

    def __init__(self, master, currPresetWidget, ipAddressWidget, maskIPWidget, gatewayIPWidget):
        super(Toolbar, self).__init__(master=master)

        self.currPresetWidget: Combobox = currPresetWidget
        self.ipAddressWidget: IPWidget = ipAddressWidget
        self.maskIPWidget: IPWidget = maskIPWidget
        self.gatewayIPWidget: IPWidget = gatewayIPWidget

        self.presetsMenu = Menu(title="Presets", tearoff=0)
        self.presetData = fileManager()

        # New Preset
        self.presetsMenu.add_command(label="Save", command=self.createNewPreset)

        # Manage Preset
        self.presetsMenu.add_command(label="Manage", command=self.managePresets)

        self.add_cascade(label="Presets", menu=self.presetsMenu)

    def createNewPreset(self):
        if self.ipAddressWidget.get().__eq__("..."):
            self.__warningBox("You must have an active IP Address")
            return
        elif self.maskIPWidget.get().__eq__("..."):
            self.__warningBox("You must have an active Mask IP")
            return
        else:
            values = {
                "ipaddress": self.ipAddressWidget.get(),
                "maskip": self.maskIPWidget.get(),
                "gatewayip": "" if self.gatewayIPWidget.get().__eq__("...") else self.gatewayIPWidget.get()}
            if not self.presetData.addPreset(title=self.currPresetWidget.get(), values=values):
                self.master.bell()
                if not messagebox.askyesno(title="WARNING", message=f"Preset {self.currPresetWidget.get()} "
                                                                    f"already exists, would you like to overwrite it?"):
                    return
                self.presetData.addPreset(title=self.currPresetWidget.get(), values=values, overwrite=True)
                messagebox.showinfo(messagebox.INFO, f"Preset {self.currPresetWidget.get()} has been "
                                                     f"changed successfully")
            else:
                messagebox.showinfo(messagebox.INFO,
                                    f"Preset {self.currPresetWidget.get()} has been added successfully")
        self.currPresetWidget.config(values=self.presetData.getTitles())

    def managePresets(self):
        if not any(isinstance(x, presetsManager) for x in self.master.winfo_children()):
            presetManager = presetsManager(master=self.master, titles=self.presetData.getTitles())
            self.wait_window(presetManager)
            if presetManager.passingData is not None:
                if not isinstance(presetManager.passingData, list):
                    self.currPresetWidget.set(presetManager.passingData)
                    self.currPresetWidget.event_generate("<<ComboboxSelected>>")
                else:
                    for preset in presetManager.passingData:
                        self.presetData.deletePreset(preset)
                    self.currPresetWidget.config(values=self.presetData.getTitles())
        else:
            for item in self.master.winfo_children():
                if isinstance(item, presetsManager):
                    item.focus()
                    self.master.bell()
                    item.state(newstate='normal')
                    break

    def writePresetsToFile(self):
        self.presetData.saveJsonData()
        self.master.destroy()

    @staticmethod
    def __warningBox(msg):
        messagebox.showinfo(messagebox.WARNING, msg)
