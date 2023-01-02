import ctypes
import os
import sys
import threading

from forms.Main import Main


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


def checkAndDeleteSetups():
    setupsPath = f"{os.environ.get('APPDATA')}/Address Modifier/"
    for file in os.listdir(setupsPath):
        if file.endswith("-setup.exe") and file.startswith("Address Modifier-"):
            print("Found!")
            print(file)
            os.remove(f"{setupsPath}/{file}")


if __name__ == "__main__":
    threading.Thread(target=checkAndDeleteSetups).start()
    if is_admin() or os.getenv("INSIDE_IDEA"):
        Main()
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv[1:]), None, 1)
