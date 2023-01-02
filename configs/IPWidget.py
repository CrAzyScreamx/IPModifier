import tkinter
from tkinter import Frame, Entry, Label
from typing import Union, List

import pyautogui


class IPWidget(Frame):

    def __init__(self, master, width: int = 3, ipHistory: Union[List, None] = None):
        super(IPWidget, self).__init__(master=master, borderwidth=1, relief="sunken",
                                       background="white")
        self.width: int = width
        self._currentFocus = 0
        self.master = master
        self._ipHistory = ipHistory
        self.currIP = 0
        self.entries = self.buildEntries()

    def buildEntries(self, amount=4):
        entries = []
        vcmd = (self.master.register(self.validateIP), '%s', '%P', '%S', '%d')
        for i in range(amount):
            entry = Entry(self, width=self.width, borderwidth=0,
                          justify="center", fg='black',
                          highlightthickness=0, background="white",
                          validate='key', validatecommand=vcmd)
            entry.pack(side="left")
            if self._ipHistory is not None:
                entry.bind("<Up>", lambda event: self.getNextIP(1))
                entry.bind("<Down>", lambda event: self.getNextIP(-1))
            entry.bind("<Left>", lambda event: self.focusPrev(event))
            entry.bind("<Right>", lambda event: self.focusNext(event))
            entry.bind("<.>", lambda event: self.moveDot(event))
            entry.bind("<FocusIn>", lambda event: self.getFocused(event))
            entries.append(entry)
            if i < amount - 1:
                dot = Label(self, text=".", background="white")
                dot.pack(side="left")
        return entries

    def validateIP(self, s, P, S, d):
        """
        :param s: before change
        :param P: after change
        :param S: the value being inserted or deleted
        :param d: 0 for attempted deletion, 1 for attempted insertion, -1 otherwise
        :return: True if passing all checks, false Otherwise
        """
        if not str(S).isdigit():
            self.master.bell()
            return False
        if len(str(P)) == 3:
            if self._currentFocus < 3:
                pyautogui.press("right")
        elif len(str(P)) > 3:
            self.master.bell()
            return False
        if int(d) == 0 and self._currentFocus > 0 and not str(s):
            pyautogui.press("left")
        return True

    def getNextIP(self, nextIP):
        if len(self._ipHistory) == 0:
            return
        print(self.currIP + nextIP)
        if self.currIP + nextIP >= len(self._ipHistory):
            self.currIP = 0
        elif self.currIP + nextIP < 0:
            self.currIP = len(self._ipHistory) - 1
        else:
            self.currIP += nextIP
        if len(self._ipHistory) > 1:
            ip = self._ipHistory[self.currIP].split(".")
            for i in range(len(self.entries)):
                ent = self.entries[i]
                ent.delete(0, "end")
                ent.insert(0, ip[i])

    def focusNext(self, event):
        entry_length = len(event.widget.get())
        cursor_pos = event.widget.index(tkinter.INSERT)
        if self._currentFocus < len(self.entries) - 1 and entry_length == cursor_pos:
            self._currentFocus += 1
            self.entries[self._currentFocus].focus()

    def focusPrev(self, event):
        cursor_position = event.widget.index(tkinter.INSERT)
        if self._currentFocus > 0 and cursor_position == 0:
            self._currentFocus -= 1
            self.entries[self._currentFocus].focus()

    def moveDot(self, event):
        if len(event.widget.get()) > 0:
            self.focusNext(event)

    def getFocused(self, event):
        self._currentFocus = self.entries.index(event.widget)

    def addToHistory(self):
        if self.get() not in self._ipHistory:
            if len(self._ipHistory) > 4:
                self._ipHistory.pop(0)
            self._ipHistory.append(self.get())

    def get(self):
        return ".".join([entry.get() for entry in self.entries])

    def switchTo(self, ip: str):
        if ip.__eq__(""):
            return
        ip = ip.split(".")
        for i in range(len(self.entries)):
            ent = self.entries[i]
            if ent.get() != ip[i]:
                ent.delete(0, "end")
                ent.insert(0, ip[i])
