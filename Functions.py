import subprocess
from threading import Timer
from tkinter import messagebox, RAISED, SUNKEN

import psutil


def btnSubmitFunc(adapterName, maskIP, ipAddress, gatewayIP, ipHistory, currPublicIP):
    try:
        address_stats = psutil.net_if_stats()[adapterName.get()]
    except KeyError:
        return errorbtn(adapterName)
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
    currPublicIP.config(text=psutil.net_if_addrs()[adapterName.get()][1][1])
    return messagebox.showinfo(messagebox.INFO, f"Updated IPv4 for {adapterName.get()} adapter")


def btnReset(adapterName, currPublicIP):
    try:
        address_stats = psutil.net_if_stats()[adapterName.get()]
    except KeyError:
        return errorbtn(adapterName)
    addressState = getattr(address_stats, "isup")
    if addressState:
        msg = messagebox.askokcancel(messagebox.WARNING, "Do you wish to proceed?")
        if msg:
            subprocess.call(f"netsh interface ipv4 set address name={adapterName.get()} source=dhcp")
            currPublicIP.config(text="Connecting...")
            Timer(10, changeAdapterLabel, [adapterName, currPublicIP]).start()
            return messagebox.showinfo(messagebox.INFO, f"Rolled Adapter {adapterName.get()} to default settings")
        else:
            return
    return errorbtn(adapterName)


def btnAOP(root , btnOnTop):
    if btnOnTop['relief'] == "sunken":
        btnOnTop.config(relief=RAISED)
        root.attributes("-topmost", False)
    else:
        btnOnTop.config(relief=SUNKEN)
        root.attributes("-topmost", True)


def changeAdapterLabel(adapterName, currPublicIP):
    currPublicIP.config(text=psutil.net_if_addrs()[adapterName.get()][1][1])


def errorbtn(adapterName):
    return messagebox.showinfo(messagebox.ERROR,
                               "Adapter might be disconnected, please check if your adapter is enabled "
                               f"( Adapter Name: {adapterName.get()} )")
