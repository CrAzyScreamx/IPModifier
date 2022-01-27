from tkinter import *
import subprocess
from typing import List
import psutil
import re

from classes import *
from tkinter import messagebox
from ttkwidgets.frames import Tooltip
from tkinter.ttk import Combobox


root = Tk()
root.title("Adapter Modifier - RADION")
ipHistory = list()

addrs = psutil.net_if_addrs()
INCs = list()
for incs in addrs.keys():
    INCs.append(re.sub("\W+ \d+", "", incs))

# this wil create a label widget
adapterNameLabel = Label(root, text="Network Adapter Name: ")
ipAddressLabel = Label(root, text="IP Address:")
maskIPLabel = Label(root, text="Mask IP:")
gatewayIPLabel = Label(root, text="Gateway IP:")
ProducedLabel = Label(root, text="Produced by Snir.Y")

# grid method to arrange labels in respective
# rows and columns as specified
adapterNameLabel.grid(row=0, column=0, sticky="ew", pady=2)
ipAddressLabel.grid(row=1, column=0, sticky="ew", pady=2)
maskIPLabel.grid(row=2, column=0, sticky="ew", pady=2)
gatewayIPLabel.grid(row=3, column=0, sticky="ew", pady=2)
ProducedLabel.grid(row=4, column=0, sticky="ew", pady=2)


def character_limit(entry_text):
    if len(entry_text.get()) > 0:
        entry_text.set(entry_text.get()[-1])


# entry widgets, used to take entry from user
# adapterName = Entry(root, width=21, fg="grey")
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


# Handle Submit Button
def btnSubmitFunc():
    netSHCmd = f"netsh interface ipv4 set address name={adapterName.get()} source=static " \
               f"address={ipAddress.get()} mask={maskIP.get()}"
    if gatewayIP.get() != "...":
        netSHCmd += f" gateway={gatewayIP.get()}"
    p = subprocess.run(netSHCmd, stdout=subprocess.PIPE)
    if not ipAddress.get() in ipHistory:
        if len(ipHistory) == 4:
            ipHistory.pop(0)
        ipHistory.insert(0, ipAddress.get())
    ipAddress.ipHistory = ipHistory
    output = p.stdout
    if output != b'\r\n':
        return messagebox.showinfo(messagebox.WARNING, output)
    return messagebox.showinfo(messagebox.INFO, f"Updated IPv4 for {adapterName.get()} adapter")


def btnAdapter():
    msg = messagebox.askokcancel(messagebox.WARNING, "Do you wish to proceed?")
    if msg:
        subprocess.call(f"netsh interface ipv4 set address name={adapterName.get()} source=dhcp")
        messagebox.showinfo(messagebox.INFO, f"Rolled Adapter {adapterName.get()} to default settings")


def btnAOP():
    if btnOnTop['relief'] == "sunken":
        btnOnTop.config(relief=RAISED)
        root.attributes("-topmost", False)
    else:
        btnOnTop.config(relief=SUNKEN)
        root.attributes("-topmost", True)


btnSubmit = Button(root, text="Submit", command=btnSubmitFunc, pady=5, width=15)
btnAdapter = Button(root, text="Reset", command=btnAdapter, pady=5, width=5, padx=5)
btnOnTop = Button(root, text="AOT", command=btnAOP)
btnSubmit.grid(row=4, column=1)
btnAdapter.grid(row=4, column=2, padx=5, pady=5)
btnOnTop.grid(row=0, column=2)

btnOnTopTT = Tooltip(btnOnTop, "", "Always On Top", timeout=0.5, offset=(1, 1), showheader=False, background="white")


# Focus In-Out Events for Entry1:
def handle_mask_focus(_):
    entries: List[Entry] = maskIP.entries
    if entries[0].get() == entries[1].get() == entries[2].get() == entries[3].get() == "":
        for i in range(0, len(entries)-1):
            entries[i].insert(0, 255)
        entries[3].insert(0, 0)


maskIP.bind("<FocusIn>", handle_mask_focus)

# infinite loop which can be terminated by keyboard
# or mouse interrupt
mainloop()
