import glob
from tkinter import *
from typing import List
import re

import Functions
from IPEntry import *
from ttkwidgets.frames import Tooltip
from tkinter.ttk import Combobox
from Functions import *


def run():
    path = "./"
    file = glob.glob(path + "/**/adm-icon.ico", recursive=True)
    root = Tk()
    root.title("Adapter Modifier - RADION")
    root.iconbitmap(default=file[0])
    ipHistory = list()

    addrs = psutil.net_if_addrs()
    print(addrs["Ethernet"][1][1])
    INCs = list()
    for incs in addrs.keys():
        INCs.append(re.sub("\W+ \d+", "", incs))

    # this wil create a label widget
    adapterNameLabel = Label(root, text="Network Adapter Name: ")
    ipAddressLabel = Label(root, text="IP Address:")
    maskIPLabel = Label(root, text="Mask IP:")
    gatewayIPLabel = Label(root, text="Gateway IP:")
    ProducedLabel = Label(root, text="Produced by Snir.Y")
    currAdapterIPStr = Label(root, text="Current Adapter's Addr: ")
    currPublicIP = Label(root, text=addrs["Ethernet"][1][1], anchor="w", font='bold')

    # grid method to arrange labels in respective
    # rows and columns as specified
    adapterNameLabel.grid(row=0, column=0, sticky="ew", pady=2)
    ipAddressLabel.grid(row=1, column=0, sticky="ew", pady=2)
    maskIPLabel.grid(row=2, column=0, sticky="ew", pady=2)
    gatewayIPLabel.grid(row=3, column=0, sticky="ew", pady=2)
    currAdapterIPStr.grid(row=4, column=0, sticky="ew", pady=2, padx=2)
    currPublicIP.grid(row=4, column=1, sticky="ew", pady=2, padx=7)
    ProducedLabel.grid(row=5, column=0, sticky="ew", pady=2)

    # entry widgets, used to take entry from user
    adapterName = Combobox(root, values=INCs)
    ipAddress = IPEntry(root, width=4, ipHistory=ipHistory)
    maskIP = IPEntry(root, width=4)
    gatewayIP = IPEntry(root, width=4)

    # this will arrange entry widgets
    adapterName.grid(row=0, column=1, padx=3)
    ipAddress.grid(row=1, column=1, padx=3)
    maskIP.grid(row=2, column=1, padx=3)
    gatewayIP.grid(row=3, column=1, padx=3)

    adapterName.insert(0, "Ethernet")
    btnSubmit = Button(root, text="Submit", command=lambda: Functions.btnSubmitFunc(adapterName, maskIP, ipAddress,
                                                                                    gatewayIP, ipHistory, currPublicIP),
                       pady=5, width=15)
    btnAdapter = Button(root, text="Reset", command=lambda: Functions.btnReset(adapterName, currPublicIP), pady=5, width=5, padx=5)
    btnOnTop = Button(root, text="AOT")
    btnSubmit.grid(row=5, column=1)
    btnAdapter.grid(row=5, column=2, padx=5, pady=5)
    btnOnTop.grid(row=0, column=2)

    btnOnTopTT = Tooltip(btnOnTop, "", "Always On Top", timeout=0.5, offset=(1, 1), showheader=False,
                         background="white")

    btnOnTop.config(command=lambda: Functions.btnAOP(root, btnOnTop))

    # Focus In-Out Events for Entry1:
    def handle_mask_focus(_):
        entries: List[Entry] = maskIP.entries
        if entries[0].get() == entries[1].get() == entries[2].get() == entries[3].get() == "":
            for i in range(0, len(entries) - 1):
                entries[i].insert(0, 255)
            entries[3].insert(0, 0)

    def onComboAdapterChange(_):
        adapter = adapterName.get()
        try:
            getDNS = psutil.net_if_addrs()[adapter][1][1]
        except KeyError:
            getDNS = "Disabled..."
        currPublicIP.config(text=getDNS)

    maskIP.bind("<FocusIn>", handle_mask_focus)
    adapterName.bind("<<ComboboxSelected>>", onComboAdapterChange)

    # infinite loop which can be terminated by keyboard
    # or mouse interrupt
    mainloop()
