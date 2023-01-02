import json
import os
from pathlib import Path
from typing import Dict, List


class fileManager:

    def __init__(self):
        self.workingDirPath = os.path.join(os.getenv("APPDATA"), "Address Modifier", "Presets.json")
        self.data: Dict = self.getOrCreateJsonData()

    def getOrCreateJsonData(self):
        self.createWorkingFolder()
        return self.getJsonData()

    def getJsonData(self):
        with open(self.workingDirPath, 'r') as f:
            return json.load(f)

    def createWorkingFolder(self):
        if os.path.exists(self.workingDirPath):
            return
        if not os.path.exists(Path(self.workingDirPath).parent):
            os.mkdir(Path(self.workingDirPath).parent)
        with open(self.workingDirPath, "w") as f:
            json.dump({'presets': {}}, f, indent=4, sort_keys=True)

    def addPreset(self, title: str, values: Dict, overwrite: bool = False) -> bool:
        """
        Adds a preset if the title is absent from the json data ( unless overwrite is enabled
        :param overwrite: If the data of the title in the json data should be overwritten
        :param title: The title of the preset
        :param values: The values of the preset, list MUST contain 3 ips
        :return: True if worked, false otherwise
        """
        if title in self.data["presets"].keys() and not overwrite:
            return False
        self.data["presets"][title] = values
        return True

    def deletePreset(self, title: str) -> bool:
        """
        Deletes a preset if it's allowed
        :param title: The title of the preset
        :return: True if deleted, false otherwise
        """
        if title not in self.data["presets"].keys():
            return False
        self.data["presets"].pop(title)

    def getPreset(self, title: str) -> Dict:
        """
        Gets a preset if it's available
        :param title: The title of the preset
        :return: The presets values
        """
        return self.data["presets"][title] if title in self.data.keys() else {}

    def saveJsonData(self):
        with open(self.workingDirPath, 'w') as f:
            json.dump(self.data, f, indent=4, sort_keys=True)

    def getTitles(self) -> List:
        return list(self.data["presets"].keys())
