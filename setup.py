from cx_Freeze import setup, Executable

target = Executable(
    script="statsIMDB.py",
    icon="icons/icon.ico",
    #shortcutName="statsIMDB",
    #shortcutDir="DesktopFolder",
    base="Win32GUI",
)

includefiles = ["icons/"]
additional_mods = ['numpy.core._methods', 'numpy.lib.format']

setup(
    name="statsIMDB",
    version="2.0",
    description="IMDB movie statistics",
    options={'build_exe': {'include_files': includefiles, 'includes': additional_mods}},
    executables=[target]
)
