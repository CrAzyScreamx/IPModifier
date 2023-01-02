import os.path
import re
import subprocess
import threading
from threading import Timer
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from typing import Tuple, List

import psutil

from configs.IPWidget import IPWidget
from configs.fileManager import fileManager
from configs.Toolbar import Toolbar
from configs.updateManager import updateManager


class Main(Tk):

    def __init__(self):
        super(Main, self).__init__(className="Address Modifier")
        self.title("Address Modifier - RADION")
        self.resizable(False, False)
        self.geometry("330x240")
        self.mainPath = os.path.dirname(__file__)
        icon = os.path.join(self.mainPath, '../Icons/default_icon.ico')
        self.iconbitmap(icon)

        self.addrProfs, self.INCs = self.getAddrProfiles()
        self.comboBoxVar = StringVar()
        self.comboBoxVar.set("Ethernet")
        self.presets = fileManager().getTitles()
        self.presetStringVar = StringVar()

        # Label widgets
        FONT = ("Arial", 11)
        self.currentPresetLabel = Label(self, text="Current Preset:", font=("Arial", 8))
        self.adapterNameLabel = Label(self, text="Network Adapter Name: ", font=FONT)
        self.ipAddressLabel = Label(self, text="IP Address: ", font=FONT)
        self.maskIPLabel = Label(self, text="Mask IP: ", font=FONT)
        self.gatewayIPLabel = Label(self, text="Gateway IP: ", font=FONT)
        self.producedByLabel = Label(self, text="Produced By Snir.Y", font=("Arial", 8))
        self.currPublicIP = Label(self, text=self.addrProfs["Ethernet"][1][1], anchor="w", font=("Bold", 15))

        # Entry widgets
        self.currentPreset = Combobox(self, values=self.presets, textvariable=self.presetStringVar,
                                      font=("Arial", 8), width=15)
        self.adapterName = Combobox(self, values=self.INCs, state="readonly", textvariable=self.comboBoxVar, width=18)
        self.ipAddress = IPWidget(self, width=4, ipHistory=[])
        self.maskIP = IPWidget(self, width=4)
        self.gatewayIP = IPWidget(self, width=4)

        # Menu
        self.toolbar = Toolbar(self, currPresetWidget=self.currentPreset, ipAddressWidget=self.ipAddress,
                               maskIPWidget=self.maskIP, gatewayIPWidget=self.gatewayIP)
        self.config(menu=self.toolbar)

        # Buttons
        self.btnSubmit = Button(self, text="Submit", command=lambda: self.changeAddr(), width=20, height=1)
        self.btnReset = Button(self, text="Reset", command=lambda: self.resetAddr(), width=20, height=1)
        self.btnSavePreset = Button(self, text="Save", command=lambda: self.toolbar.createNewPreset())
        self.btnAOT = Button(self, text="AOT", command=lambda: self.alwaysOnTop())

        LAYOUT_RATIO = 5
        # Label Placements
        self.currentPresetLabel.place(x=10, y=LAYOUT_RATIO)
        self.adapterNameLabel.place(x=10, y=LAYOUT_RATIO + 30)
        self.ipAddressLabel.place(x=89, y=LAYOUT_RATIO + 55)
        self.maskIPLabel.place(x=108, y=LAYOUT_RATIO + 80)
        self.gatewayIPLabel.place(x=85, y=LAYOUT_RATIO + 105)
        self.currPublicIP.place(relx=0.5, y=LAYOUT_RATIO + 150, anchor=CENTER)
        self.producedByLabel.place(x=10, y=LAYOUT_RATIO + 195)

        # Entry Placements
        self.currentPreset.place(x=88, y=LAYOUT_RATIO)
        self.adapterName.place(x=173, y=LAYOUT_RATIO + 32)
        self.ipAddress.place(x=173, y=LAYOUT_RATIO + 57)
        self.maskIP.place(x=173, y=LAYOUT_RATIO + 82)
        self.gatewayIP.place(x=173, y=LAYOUT_RATIO + 107)

        # Btn Placements
        self.btnSubmit.place(x=10, y=LAYOUT_RATIO + 170)
        self.btnReset.place(x=170, y=LAYOUT_RATIO + 170)
        self.btnSavePreset.place(x=205, y=LAYOUT_RATIO, height=20, width=40)
        self.btnAOT.place(x=285, y=LAYOUT_RATIO, height=20, width=40)

        # Binds
        self.adapterName.bind("<<ComboboxSelected>>", self.onComboChange)
        self.currentPreset.bind("<<ComboboxSelected>>", self.switchToPreset)
        self.maskIP.bind("<FocusIn>", self.onMaskHandler)

        self.protocol("WM_DELETE_WINDOW", self.toolbar.writePresetsToFile)

        # Upgrade
        self.upgradeManager = updateManager()

        def checkAppVersion():
            if not self.upgradeManager.checkApplicationVersion():
                self.showUpgradeProgress()

        threading.Thread(target=checkAppVersion).start()

        self.mainloop()

    @staticmethod
    def getAddrProfiles() -> Tuple:
        addr = psutil.net_if_addrs()
        INCs = [re.sub("\W+ \d+", "", incs) for incs in addr.keys()]
        return addr, INCs

    def changeAddr(self):
        try:
            address = psutil.net_if_stats()[self.adapterName.get()]
        except KeyError as e:
            return self.sendError(f"Adapter is disconnected or no longer available ({self.adapterName.get()})")
        if not getattr(address, "isup"):
            return self.sendError(f"Adapter is disconnected or no longer available ({self.adapterName.get()})")
        netSHCmd = f"netsh interface ipv4 set address name=\"{self.adapterName.get()}\" source=static " \
                   f"address={self.ipAddress.get()} mask={self.maskIP.get()}"
        if not self.gatewayIP.get().__eq__("..."):
            netSHCmd += f" gateway={self.gatewayIP.get()}"
        process = subprocess.run(netSHCmd, stdout=subprocess.PIPE)
        output = process.stdout
        if output != b'\r\n':
            return messagebox.showinfo(messagebox.WARNING, output)
        self.ipAddress.addToHistory()
        self.currPublicIP.config(text=psutil.net_if_addrs()[self.adapterName.get()][1][1])
        return messagebox.showinfo(messagebox.INFO, f"Updated IPV4 for adapter {self.adapterName.get()}")

    def resetAddr(self):
        try:
            address = psutil.net_if_stats()[self.adapterName.get()]
        except KeyError:
            return self.sendError(f"Adapter is disconnected or no longer available ({self.adapterName.get()})")
        if not getattr(address, "isup"):
            return self.sendError(f"Adapter is disconnected or no longer available ({self.adapterName.get()})")
        if messagebox.askyesno(messagebox.WARNING, "Do you wish to proceed?"):
            process = subprocess.run(f"netsh interface ipv4 set address name=\"{self.adapterName.get()}\" source=dhcp",
                                     stdout=subprocess.PIPE)
            if process.stdout.startswith(b'DHCP is already'):
                return self.sendError(process.stdout)
            self.btnSubmit.config(state=DISABLED)
            self.currPublicIP.config(text="Connecting...")
            Timer(10, self.changeAdapterLabel).start()
            return messagebox.showinfo(messagebox.INFO, f"Rolled Adapter {self.adapterName.get()} to default "
                                                        f"settings")

    @staticmethod
    def sendError(msg):
        return messagebox.showinfo(messagebox.ERROR,
                                   msg)

    def onComboChange(self, _):
        adapter = self.adapterName.get()
        try:
            getDNS = psutil.net_if_addrs()[adapter][1][1]
        except KeyError:
            getDNS = "Disabled..."
        self.currPublicIP.config(text=getDNS)

    def switchToPreset(self, _):
        def presetThreadFunc():
            data = self.toolbar.presetData.data["presets"][self.presetStringVar.get()]
            self.ipAddress.switchTo(data["ipaddress"])
            self.maskIP.switchTo(data["maskip"])
            self.gatewayIP.switchTo(data["gatewayip"])

        t = threading.Thread(target=presetThreadFunc)
        t.start()

    def onMaskHandler(self, _):
        entries: List[Entry] = self.maskIP.entries
        if entries[0].get() == entries[1].get() == entries[2].get() == entries[3].get() == "":
            for i in range(len(entries) - 1):
                entries[i].insert(0, 255)
            entries[3].insert(0, 0)

    def alwaysOnTop(self):
        if self.btnAOT['relief'] == "sunken":
            self.btnAOT.config(relief=RAISED)
            self.attributes("-topmost", False)
        else:
            self.btnAOT.config(relief=SUNKEN)
            self.attributes("-topmost", True)

    def changeAdapterLabel(self):
        self.currPublicIP.config(text=psutil.net_if_addrs()[self.adapterName.get()][1][1])
        self.btnSubmit.config(state=ACTIVE)

    def showUpgradeProgress(self):
        if messagebox.askyesno(title="NEW UPDATE", message=f"There is a new Update available "
                                                           f"({self.upgradeManager.latestVersion}), "
                                                           f"do you wish to download it?"):
            self.withdraw()
            self.upgradeManager.showProgWindow(self)
            subprocess.Popen([f"{os.environ.get('APPDATA')}/Address Modifier/"
                              f"Address Modifier-{self.upgradeManager.installedInstallVersion}-setup.exe"])
            self.quit()
