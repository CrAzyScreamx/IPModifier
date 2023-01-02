import os
from configparser import ConfigParser
from paramiko import Transport, SFTPClient
from tkinter.ttk import Progressbar
from tkinter import Label, Toplevel


class updateManager:

    def __init__(self):

        self.remotePath = "/home/sftpuser/apps/nifty-tesla285/code_server_volume/workspace/Address Modifier"
        self.localPath = os.path.join(os.environ.get("Appdata"), "Address Modifier")

        self.configINIFile = ConfigParser()
        self.configINIFile.read(os.path.join(self.localPath, "update.ini"))

        # Remote Connection
        self.hostPortTuple = ("185.248.134.134", 10716)
        self.username, self.password = "sftpuser", "zaLMd4Fy5PdEDg"

        # Version
        self.latestVersion = None
        self.installedInstallVersion = None

        # Widgets
        self.window = None
        self.label = None
        self.progBar = None

    def checkApplicationVersion(self):
        currVersion = self.__getCurrAppVersion()
        self.latestVersion = self.__getRemoteAppVersion()
        return currVersion.__eq__(self.latestVersion)

    def showProgWindow(self, master):
        self.window = Toplevel(master=master)
        self.window.grab_set()
        self.window.geometry("200x50")
        self.label = Label(self.window, text="0/0 downloaded")
        self.label.pack()
        self.progBar = Progressbar(self.window, mode="determinate", length=100)
        self.progBar.config(value=0)
        self.progBar.pack()
        self.__downloadSetup()
        self.window.destroy()

    def __showProgress(self, transferred, total):
        self.label.config(text=f"{self.bytesToMB(transferred)}/{self.bytesToMB(total)} downloaded")
        self.progBar.config(value=(transferred/total)*100)

    def __downloadSetup(self, version=None):
        if version is None:
            version = self.__getRemoteAppVersion()
        self.installedInstallVersion = version

        def __downloadVersionFromSFTP(sftp: SFTPClient):
            setupString = f"Address Modifier-{version}-setup.exe"
            sftp.get(f"{self.remotePath}/{setupString}",
                     f"{self.localPath}/{setupString}", callback=self.__showProgress)
            return f"{self.remotePath}/{setupString}"

        return self.__runFunctionToConnectedServer(__downloadVersionFromSFTP)

    def __getCurrAppVersion(self) -> str:
        return self.configINIFile.get("Settings", "Version")

    def __getRemoteAppVersion(self) -> str:
        def __readFileContents(sftp):
            file = sftp.open(f"{self.remotePath}/latest.txt", 'r')
            contents = file.read()
            return contents.decode("UTF-8")

        return self.__runFunctionToConnectedServer(__readFileContents)

    def __runFunctionToConnectedServer(self, function, *args):
        transport = Transport(self.hostPortTuple)
        transport.connect(username=self.username, password=self.password)
        with SFTPClient.from_transport(transport) as sftp:
            result = function(sftp, *args)
            sftp.close()
        transport.close()
        return result

    @staticmethod
    def bytesToMB(amount):
        amount = float(amount / 1048576)
        return round(amount, 2)
