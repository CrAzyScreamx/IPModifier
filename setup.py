import json
import sys
from cx_Freeze import setup, Executable

with open('opts.json', 'r') as f:
    opts = json.load(f)

base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [Executable("Address Modifier.py", base=base, icon="adm-icon.ico")]

setup(
    name="IPModifier - RADION",
    version="0.1",
    description="Changes DNS Types using a click of Button",
    options={"build_exe": opts["build_exe_options"]},
    executables=executables,
)
