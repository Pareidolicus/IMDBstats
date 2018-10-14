from cx_Freeze import setup, Executable

target = Executable(
    script="statsIMDB.py",
    icon="icon.ico",
    #shortcutName="statsIMDB",
    #shortcutDir="DesktopFolder",
    base="Win32GUI",
)

includefiles = ["icon.ico", "config.ini"]

setup(
    name="statsIMDB",
    version="1.0",
    description="IMDB movie statistics",
    options={'build_exe': {'include_files': includefiles}},
    executables=[target]
)
