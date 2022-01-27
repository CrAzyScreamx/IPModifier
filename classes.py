import tkinter as tk
import win32com.client as comclt

wsh = comclt.Dispatch("WScript.shell")


class IPEntry(tk.Frame):
    def __init__(self, parent, width=3, ipHistory=None):
        tk.Frame.__init__(self, parent, borderwidth=1, relief="sunken",
                          background="white")
        self.parent = parent
        vcmd = (parent.register(self.validate), '%S', '%s', '%d')
        self._entries = []
        self.width = width
        self._ipHistory = ipHistory
        self.countIps = 0
        for i in range(4):
            entry = tk.Entry(self, width=width, borderwidth=0,
                             justify="center", fg='black',
                             highlightthickness=0, background="white",
                             validate='key', validatecommand=vcmd)
            entry.pack(side="left")
            if not ipHistory is None:
                entry.bind("<Up>", lambda event: self.key_pressed(event, 1))
                entry.bind("<Down>", lambda event: self.key_pressed(event, -1))
            self._entries.append(entry)
            if i < 3:
                dot = tk.Label(self, text=".", background="white")
                dot.pack(side="left")

    @property
    def entries(self):
        return self._entries

    @entries.setter
    def entries(self, value):
        self._entries = value

    @property
    def ipHistory(self):
        return self._ipHistory

    @ipHistory.setter
    def ipHistory(self, value):
        self._ipHistory = value

    def get(self):
        return ".".join([entry.get() for entry in self._entries])

    def validate(self, S, s, d):
        if not is_Integer(S):
            self.parent.bell()
            return False
        nowLetter = int(str(s) + str(S))
        if (len(s) == 1 and int(d) == 0) \
                or (is_Integer(S) and
                    nowLetter < 256 and
                    len(s) < 3) \
                or int(d) != 1:
            return True
        self.parent.bell()
        return False

    def key_pressed(self, event, nextInList):
        if self.countIps >= len(self._ipHistory):
            self.countIps = 0
        if self.countIps < 0:
            self.countIps = len(self._ipHistory) - 1
        if len(self._ipHistory) > 0:
            ip = self._ipHistory[self.countIps].split(".")
            for i in range(len(self._entries)):
                ent = self._entries[i]
                ent.delete(0, "end")
                ent.insert(0, ip[i])
            self.countIps += nextInList


def is_Integer(val):
    try:
        val = int(val)
    except ValueError:
        return False
    return True
