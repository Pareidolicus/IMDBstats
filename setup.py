from cx_Freeze import setup, Executable

target = Executable(
    script="statsIMDB.py",
    icon="icon.ico",
    base="Win32GUI",
)

includefiles = ["icon.ico"]

setup(
    name="statsIMDB",
    version="0.1",
    description="IMDB movie statistics",
    options={'build_exe': {'include_files': includefiles}},
    executables=[target]
)
